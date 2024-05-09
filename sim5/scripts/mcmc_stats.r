
library(tools)
library(TraceR)
library(readr)


mcmc_path <- "/Users/xuyuan/workspace/py/pythonProject1/sim5/beast"
output_path <- "/Users/xuyuan/workspace/py/pythonProject1/sim5/stats"

burnin <- 0.1
files <- dir(path=mcmc_path, pattern=".log")

for (f in files) {
	mcmc_log <- readMCMCLog(file.path(mcmc_path, f))
	traces <- getTraces(mcmc_log, burn.in=burnin)
	stats <- analyseTraces(traces)
    output_file <- file.path(output_path, paste0(file_path_sans_ext(basename(f)), "_stats.log"))
	write_tsv(stats, out)
}