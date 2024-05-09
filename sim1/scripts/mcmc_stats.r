library("tools")
library("TraceR")
# library(readr)

//mcmc_path <- "../beast"
# mcmc_path <- "/Users/xuyuan/workspace/yxu927/untitled/sim1/beast"(全是log文件mcmc的，nesi输出的)
# output_path <- "/Users/xuyuan/workspace/yxu927/untitled/sim1/stats"(全是true文件原始的)

mcmc_path <- "/Users/xuyuan/workspace/py/pythonProject1/sim1/beast"
output_path <- "/Users/xuyuan/workspace/py/pythonProject1/sim1/stats"

burnin <- 0.1
files <- dir(path=mcmc_path, pattern=".log")

for (f in files) {
	mcmc_log <- readMCMCLog(file.path(mcmc_path, f))
	traces <- getTraces(mcmc_log, burn.in=burnin)
	stats <- analyseTraces(traces)
	out <- paste0(file_path_sans_ext(basename(f)), "_stats.log")

#     output_file <- file.path(output_path, paste0(file_path_sans_ext(basename(f)), "_stats.log"))
	write_tsv(stats, out)
}

