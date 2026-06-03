module mod_initial
    use iso_fortran_env, only : int32, real32
    implicit none

contains
    pure subroutine set_gaussian(x, icenter, decay)
        real(kind=real32), intent(inout) :: x(:)
        integer(kind=int32), intent(in) :: icenter
        real(kind=real32), intent(in) :: decay
        integer(kind=int32) :: i
        do concurrent(i = 1:size(x))
            x(i) = exp(-decay * (i-icenter)**2)
        end do
    end subroutine set_gaussian

end module mod_initial