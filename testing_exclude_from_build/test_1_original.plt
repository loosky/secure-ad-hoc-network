set term png size 480,360
set yrange [0.5:4.5]
set ylabel "Time (sec)"
set xlabel "Run (#)"
set output 'test_1_original.png'
set lmargin 9
set rmargin 1
set tmargin 1

plot 'plot-test1-original.dat' u 1:2 t 'Both Nodes Added' w linespoint, 'plot-test1-original.dat' u 1:3 t 'First Node Added' w linespoint
