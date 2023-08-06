#pragma once

#include "supermode.cpp"
#include "extrapolate.cpp"
#include "progressbar.cpp"
#include "laplacian.cpp"
#include "definitions.cpp"
#include "utils.cpp"
#include "numpy_interface.cpp"

class CppSolver : public BaseLaplacian
{
    public:
        size_t n_computed_mode, n_sorted_mode, max_iteration, iteration, nx, ny, n_slice;
        double tolerance, k_initial, wavelength, d_itr;
        std::vector<SuperMode> computed_supermodes, sorted_supermodes;
        bool show_iteration, show_eigenvalues;
        Eigen::MatrixXd previous_eigen_vectors;
        Eigen::VectorXd previous_eigen_values, itr_list, mesh_gradient;
        std::vector<double> alpha_vector;

    CppSolver(
        pybind11::array_t<double> &mesh_py,
        pybind11::array_t<double> &mesh_gradient_py,
        std::vector<std::vector<double>> &finit_difference_matrix,
        pybind11::array_t<double> &itr_list_py,
        size_t n_computed_mode,
        size_t n_sorted_mode,
        size_t max_iteration,
        double tolerance,
        double wavelength,
        bool show_iteration,
        bool show_eigenvalues)
        : BaseLaplacian(mesh_py, finit_difference_matrix),
          max_iteration(max_iteration), tolerance(tolerance), n_sorted_mode(n_sorted_mode),
          n_computed_mode(n_computed_mode), wavelength(wavelength),
          show_iteration(show_iteration), show_eigenvalues(show_eigenvalues)
    {
        this->k_initial = 2.0 * PI / wavelength;
        this->nx = mesh_gradient_py.request().shape[0];
        this->ny = mesh_gradient_py.request().shape[1];
        this->n_slice = itr_list_py.size();

        double *itr_list_ptr = (double*) itr_list_py.request().ptr;
        Eigen::Map<Eigen::VectorXd> mapping_itr_list(itr_list_ptr, n_slice);
        this->itr_list = mapping_itr_list;

        double *mesh_gradient_ptr = (double*) mesh_gradient_py.request().ptr;
        Eigen::Map<Eigen::VectorXd> mapping_mesh_gradient(mesh_gradient_ptr, nx * ny);
        this->mesh_gradient = mapping_mesh_gradient;

        this->d_itr = abs(itr_list[1] - itr_list[0]);

        this->generate_mode_set();
    }


   SuperMode &get_sorted_mode(size_t mode_number){ return sorted_supermodes[mode_number]; }

   void generate_mode_set()
   {
     for (int mode_number=0; mode_number<n_computed_mode; ++mode_number)
        computed_supermodes.push_back(SuperMode(mode_number, k_initial, mesh_gradient, itr_list, nx, ny));

     for (int mode_number=0; mode_number<n_sorted_mode; ++mode_number)
        sorted_supermodes.push_back( SuperMode(mode_number, k_initial, mesh_gradient, itr_list, nx, ny));
   }

    tuple<Eigen::MatrixXd, Eigen::VectorXd> compute_eigen_solution(const double &alpha){

        this->compute_finit_diff_matrix();

        Spectra::SparseGenRealShiftSolve<double> op(eigen_matrix);

        Spectra::GenEigsRealShiftSolver<Spectra::SparseGenRealShiftSolve<double>> eigs(
            op,
            n_computed_mode,
            n_computed_mode + 3 ,
            alpha
        );

        eigs.init();

        int nconv = eigs.compute(
            Spectra::SortRule::LargestMagn,
            this->max_iteration,
            this->tolerance,
            Spectra::SortRule::LargestMagn
        );

        eigen_matrix.resize(0,0);

        Eigen::MatrixXd eigen_vectors = eigs.eigenvectors().real();
        Eigen::VectorXd eigen_values = eigs.eigenvalues().real();

        this->sort_eigen_decomposition(eigen_vectors, eigen_values);

        return std::make_tuple(eigen_vectors, eigen_values);
    }

    void sort_eigen_decomposition(Eigen::MatrixXd& eigen_vectors, Eigen::VectorXd& eigen_values)
    {
        if (this->iteration != 0)
            this->sort_eigen_with_fields(eigen_vectors, eigen_values);

        previous_eigen_values = eigen_values.block(0, 0, n_sorted_mode, 1);
        previous_eigen_vectors = eigen_vectors.block(0, 0, this->nx * this->ny, n_sorted_mode);
    }

    void sort_eigen_with_fields(Eigen::MatrixXd& eigen_vectors, Eigen::VectorXd& eigen_values)
    {
        Eigen::Index max_index;

        Eigen::MatrixXd overlap_matrix = (previous_eigen_vectors.transpose() * eigen_vectors).cwiseAbs();
        Eigen::MatrixXd temporary_vector = eigen_vectors;
        Eigen::VectorXd temporary_value = eigen_values;


        for (size_t mode_0=0; mode_0<n_sorted_mode; ++mode_0)
        {
            double best_overlap = overlap_matrix.row(mode_0).maxCoeff(&max_index);

            if (best_overlap < 0.8)
                std::cout<<"Warning: bad mode field matching"
                         <<"\titeration: "<<this->iteration
                         <<"overlap matrix: \n"<<overlap_matrix<<"\n"
                         <<"mode index: "<<mode_0
                         <<"max_index: "<<max_index<<"\n\n";

            eigen_vectors.col(mode_0) = temporary_vector.col(max_index);
            eigen_values.row(mode_0) = temporary_value.row(max_index);

            overlap_matrix.col(max_index) *= 0;
        }
    }

    void populate_sorted_supermodes(size_t slice, Eigen::MatrixXd& eigen_vectors, Eigen::VectorXd& eigen_values)
    {
        for (SuperMode& mode : sorted_supermodes)
        {
            mode.eigen_value[slice] = eigen_values[mode.mode_number];
            mode.fields.col(slice) << eigen_vectors.col(mode.mode_number);

            mode.betas[slice] = sqrt( abs(mode.eigen_value[slice]) ) / itr_list[slice];
            mode.index[slice] = mode.betas[slice] / k_initial;
        }
    }


    void loop_over_itr(size_t extrapolation_order = 1, double alpha = 0)
    {
        this->iteration = 0;
        Eigen::MatrixXd eigen_vectors;
        Eigen::VectorXd eigen_values;

        Extrapolator extrapolator = Extrapolator(d_itr, extrapolation_order);

        ProgressBar progress_bar = ProgressBar(itr_list.size(), 70, show_iteration, true);

        alpha_vector.reserve(itr_list.size());

        if (alpha == 0)
            alpha = -pow(this->k_initial * this->compute_max_index(), 2);

        for (size_t slice=0; slice<itr_list.size(); ++slice)
        {
            progress_bar.show_next(itr_list[slice]);

            k_taper = this->k_initial * itr_list[slice];

            tie(eigen_vectors, eigen_values) = this->compute_eigen_solution(alpha);

            if (show_eigenvalues)
            {
                std::cout.precision(16);
                std::cout<<" alpha guess: "<<alpha<<"\t"
                <<eigen_values.transpose()
                <<"\n";
            }

            this->populate_sorted_supermodes(slice, eigen_vectors, eigen_values);

            alpha_vector.insert(alpha_vector.begin(), eigen_values[0]);

            alpha = extrapolator.extrapolate_next(alpha_vector);

            this->iteration++;
        }
        this->arrange_mode_field();
    }

    void arrange_mode_field()
    {
        std::cout<<"Regularizing mode fields\n";

        for (size_t mode=0; mode<n_sorted_mode; ++mode)
        {
            SuperMode &Mode = sorted_supermodes[mode];
            for (size_t slice=0; slice<itr_list.size()-2; ++slice)
            {
                double overlap = Mode.compute_overlap(Mode, slice, slice+1);
                if (overlap < 0)
                    Mode.fields.col(slice+1) *= -1;
            }
        }
    }

   double compute_max_index()
   {
     double max_index = 0.0;
     for (size_t i=0; i<size; ++i)
        if (meshPtr[i] > max_index)
            max_index = meshPtr[i];

    return max_index;
   }
};
