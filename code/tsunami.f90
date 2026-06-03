program tsunami
    use iso_fortran_env, only: int32, real32
    use mod_diff, only: diff => diff_centered
    use mod_initial, only: set_gaussian
    implicit none

    real(kind=real32), parameter :: g = 9.81
    

    integer(kind=int32) :: n
    integer(kind=int32), parameter:: nx=100 , nt=5000
    real(kind=real32), parameter :: dt = 0.02, dx = 1.
    real(kind=real32) :: h(nx), u(nx)

    real(kind=real32) :: hmean = 10

    ! set up initial condition
    integer(kind=int32), parameter :: icenter = 25
    real(kind=real32), parameter :: decay = 0.02


    call set_gaussian(h, icenter, decay)
    u=0
    
    time_loop: do n = 1, nt
        u = u - (u*diff(u) + g*diff(h))/dx * dt

        h = h - diff(u*(hmean+h))/dx * dt

        print *, n, h
    end do time_loop
    
    print *, n, h

end program 