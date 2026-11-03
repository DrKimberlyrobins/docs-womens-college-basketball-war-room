#!/usr/bin/env Rscript
# Historical, pre-tip season 2026 ratings from SportsDataverse wehoop.
# 2026 is the 2025-26 season; 2027 is 2026-27.
suppressPackageStartupMessages(library(wehoop))
suppressPackageStartupMessages(library(jsonlite))
suppressPackageStartupMessages(library(dplyr))
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 1) stop("Pass destination CSV")
ratings <- load_wbb_ratings(seasons=2026)
if (nrow(ratings)==0) stop("wehoop returned no historical ratings")
write.csv(ratings, args[1], row.names=FALSE, na="")
cat("Downloaded",nrow(ratings),"historical ratings rows; columns:",paste(names(ratings),collapse=","),"\n")
