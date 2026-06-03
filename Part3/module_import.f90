program print_compiler_info
    use iso_fortran_env
    implicit none
    print *, 'compiler version: ', compiler_version()
    print *, 'compiler options: ', compiler_options()
end program print_compiler_info