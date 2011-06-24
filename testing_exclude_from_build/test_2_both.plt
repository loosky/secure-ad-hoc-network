set term png size 480,360
set ylabel "Time (sec)"
set xlabel "Run (#)"
set output 'test_2.png'
set lmargin 9
set rmargin 1
set tmargin 1

plot 'plot-test2-original.dat' u 1:2 t 'Original B.A.T.M.A.N.' w linespoint, 'plot-test2-secure.dat' u 1:2 t 'Modified B.A.T.M.A.N.' w linespoint
