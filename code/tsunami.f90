program tsunami
    implicit none
    

    integer :: n
    integer, parameter:: nx=100 , nt=100

    real, parameter :: dt = 1., dx = 1., c = 1.
    real :: h(nx), dh(nx)

    ! set up initial condition
    integer, parameter :: icenter = 25
    real, parameter :: decay = 0.02


    call set_gaussian(h, icenter, decay)
    
    time_loop: do n = 1, nt
        dh(1) = h(1) - h(nx)
        
        h = h - c*diff(h) / dx * dt

        print *, n, h
    end do time_loop
    
    print *, n, h

    contains

    function diff(x) result (dx)
        real, intent(in) :: x(:)
        real :: dx(size(x))
        integer :: im

        im = size(x)
        dx(1) = x(1) - x(im)
        dx(2:im) = x(2:im) - x(1:im-1)
    end function diff

    subroutine set_gaussian(x, icenter, decay)
        real, intent(inout) :: x(:)
        integer, intent(in) :: icenter
        real, intent(in) :: decay
        integer :: i
        do concurrent(i = 1:size(x))
            x(i) = exp(-decay * (i-icenter)**2)
        end do
    end subroutine set_gaussian
        

end program 