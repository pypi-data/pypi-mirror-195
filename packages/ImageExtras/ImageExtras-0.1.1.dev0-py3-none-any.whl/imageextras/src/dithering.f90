subroutine FS (img, th, size_x, size_y, img_out)

    implicit none

    integer, intent(in) :: size_x, size_y
    real (kind = 8), dimension(size_x,size_y), intent(in) :: img
    real (kind = 8), intent(in) :: th
    real (kind = 8), dimension(size_x,size_y), intent(out) :: img_out

    integer :: row = 1, column = 1
    real (kind = 8), dimension(1) :: err_m, val_max
    real (kind = 8) :: err

    img_out = img

    val_max = maxval(img)

    do row = 2, (size_x - 1)
        
        do column = 2, (size_y - 1)

            if (img_out(row, column) .GT. th) then
                
                err_m = img_out(row, column)
                err = err_m(1) - val_max(1)

            else
                
                err = img_out(row, column)

            end if
                
            img_out(row, column+1) = img_out(row, column+1) + 7./16. * err
            img_out(row+1, column-1) = img_out(row+1, column-1) + 3./16. * err
            img_out(row+1, column) = img_out(row+1, column) + 5./16. * err
            img_out(row+1, column+1) = img_out(row+1, column+1) + 1./16. * err

            !img_out(row+1, column) = img(row+1, column) + 7./16. * err
            !img_out(row-1, column+1) = img(row-1, column+1) + 3./16. * err
            !img_out(row, column+1) = img(row, column+1) + 5./16. * err
            !img_out(row+1, column+1) = img(row+1, column+1) + 1./16. * err
            
        end do

    end do

end subroutine

subroutine JJN (img, th, size_x, size_y, img_out)

    implicit none

    integer, intent(in) :: size_x, size_y
    real (kind = 8), dimension(size_x,size_y), intent(in) :: img
    real (kind = 8), intent(in) :: th
    real (kind = 8), dimension(size_x,size_y), intent(out) :: img_out

    integer :: row = 1, column = 1
    real (kind = 8), dimension(1) :: err_m, val_max
    real (kind = 8) :: err

    img_out = img

    val_max = maxval(img)

    do row = 3, (size_x - 2)
        
        do column = 3, (size_y - 2)

            if (img_out(row, column) .GT. th) then
                
                err_m = img_out(row, column)
                err = err_m(1) - val_max(1)

            else
                
                err = img_out(row, column)

            end if
                
            img_out(row, column+1) = img_out(row, column+1) + 7./48. * err
            img_out(row, column+2) = img_out(row, column+2) + 5./48. * err

            img_out(row+1, column-2) = img_out(row+1, column-2) + 3./48. * err
            img_out(row+1, column-1) = img_out(row+1, column-1) + 5./48.  * err
            img_out(row+1, column) = img_out(row+1, column) + 7./48.  * err
            img_out(row+1, column+1) = img_out(row+1, column+1) + 5./48.  * err
            img_out(row+1, column+2) = img_out(row+1, column+2) + 3./48.  * err
            
            img_out(row+2, column-2) = img_out(row+2, column-2) + 1./48.  * err
            img_out(row+2, column-1) = img_out(row+2, column-1) + 3./48.  * err
            img_out(row+2, column) = img_out(row+2, column) + 5./48.  * err
            img_out(row+2, column+1) = img_out(row+2, column+1) + 3./48.  * err
            img_out(row+2, column+2) = img_out(row+2, column+2) + 1./48.  * err
            
        end do

    end do

end subroutine