#!/bin/sh -vx

rm results/*
rm log/*
rm *.tar
tar czf data.tar data
condor_submit menom_mc.sub

