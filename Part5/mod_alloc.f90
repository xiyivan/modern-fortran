module mod_alloc
    implicit none

    private
    public :: alloc, free
    
contains
    subroutine alloc(a, n)
        real, allocatable, intent(inout) :: a(:)
        integer, intent(in) :: n
        if (allocated(a)) deallocate(a)
        allocate(a(n))
    end subroutine

    subroutine free(a)
        real, allocatable, intent(inout) :: a(:)
        if (allocated(a)) deallocate(a)
    end subroutine
    
end module mod_alloc