program cold_front
    
    implicit none

    real :: T_Atlanta, T_Miami
    real, parameter :: x = 960, v = 20
    real :: t
    integer :: i

    T_Atlanta = 12
    T_Miami = 24

    do i = 1, (48/6)
        t = i * 6.0
        print *, "Temperature after", t, "hours is ", cold_front_temperature(T_Atlanta, T_Miami, v, x, t), "degrees."
    end do
    
    contains

    real function cold_front_temperature(temp1, temp2, c, dx, dt) result(final_temp)
        real, intent(in) :: temp1, temp2, c, dx, dt 
        
        final_temp = temp2 + (temp1 - temp2)/dx * c * dt
    end function cold_front_temperature



end program cold_front

    
