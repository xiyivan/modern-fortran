program tsunami
    implicit none
    

    integer :: i, n
    integer, parameter:: nx=100 , nt=100

    real, parameter :: dt = 1., dx = 1., c = 1.
    real :: h(nx), dh(nx)

    ! set up initial condition
    integer, parameter :: icenter = 25
    real, parameter :: decay = 0.02


    do concurrent (i = 1:nx) 
        h(i) = exp(-decay * (i-icenter)**2)
    end do
    
    time_loop: do n = 1, nt
        dh(1) = h(1) - h(nx)
        
        do concurrent (i = 2:nx)
            dh(i) = h(i) - h(i-1)
        end do

        do concurrent (i = 1:nx)
            h(i) = h(i) - c*dh(i) / dx * dt
        end do

        print *, n, h
    end do time_loop
    
    print *, n, h
end program 