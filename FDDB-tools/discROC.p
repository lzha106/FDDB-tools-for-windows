# Compare your discrete ROC curves with other methods
# At terminal: gnuplot discROC.p
set terminal png size 1280, 960 enhanced font 'Verdana,18'
set size 1,1
set xtics 100
set ytics 0.1
set grid
set ylabel "True positive rate"
set xlabel "False positive"
set xr [0:1000]
set yr [0:1.0]
set key below
set output "discROC-compare.png"
plot  "../mtcnn_fddb/DiscROC.txt" using 2:1 title 'test' with lines lw 2


 
