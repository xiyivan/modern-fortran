program stock_volatility
    use mod_array, only: average, std, moving_average, moving_std, reverse
    use mod_io, only: read_stock, write_stock

    implicit none

    character(len=4), allocatable :: symbols(:)
    character(len=:), allocatable :: time(:)
    real, allocatable :: open(:), high(:), low(:), close(:), adjclose(:), volume(:)

    integer :: n, im

    symbols = ['AAPL', 'AMZN', 'CRAY', 'CSCO', 'HPQ ', 'IBM ', 'INTC', 'MSFT', 'NVDA', 'ORCL']
    

    do n = 1, size(symbols)
        call read_stock('data/' // trim(symbols(n)) // '.csv', &
        time, open, high, low, close, adjclose, volume)

        im = size(time)
        adjclose = reverse(adjclose)
        time = time(im:1:-1)
        call write_stock(trim(symbols(n)) // '_volatility.txt', time, adjclose, &
            moving_average(adjclose, 30), moving_std(adjclose, 30))
    end do
end program stock_volatility
