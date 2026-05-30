program array_copy_caf
	implicit none

	integer :: array(5) [*] = 0
	integer, parameter :: sender = 1, receiver = 2

	if (this_image() == sender) then
		array = [1, 2, 3, 4, 5]
	endif
		
	print '(a, i2, a, 5(4x, i2))', "Array on Proc ", this_image(), "before sync is", array

	sync all

	if (this_image() == receiver) then
		array = array(:)[sender]
	endif

	print '(a, i2, a, 5(4x, i2))', "Array on Proc ", this_image(), "after sync is", array
end program
