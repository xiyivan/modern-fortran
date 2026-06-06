program stock_crossover
    use mod_io, only: read_stock, write_stock
    use mod_array, only: moving_average, crosspos, crossneg

    implicit none

    character(len=4), allocatable :: symbols(:)
    character(len=:), allocatable :: time(:)
    real, allocatable :: open(:), high(:), low(:), close(:), adjclose(:), volume(:)

    integer :: i, n, fileunit
    integer, allocatable :: buy(:), sell(:)

    symbols =  ['AAPL', 'AMZN', 'CRAY', 'CSCO', 'HPQ ', 'IBM ', 'INTC', 'MSFT', 'NVDA', 'ORCL']

    

    do i = 1, size(symbols)
        call read_stock('data/' // trim(symbols(i)) // '.csv', time, open, high, low, close ,adjclose, volume)

        buy = crosspos(adjclose, 30)
        sell = crossneg(adjclose, 30)

        open(newunit=fileunit, file=trim(symbols(i))//"_crossover.txt")
        do n = 1, size(buy)
            write(fileunit, fmt=*) "Buy", time(buy(n))
        end do

        do n = 1, size(sell)
            write(fileunit, fmt=*) "Sell", time(sell(n))
        end do
        close(fileunit)
    end do
end program stock_crossover        