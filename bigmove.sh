#!/bin/sh

scp -r LdF_Diff_OTB/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Diff_OTB/.
scp -r LdF_SE_OTB/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_SE_OTB/.
scp -r LdF_LGBK_OTB/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_LGBK_OTB/.
scp -r LdF_Main_current/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Main_current/.
scp -r LdF_Main_future/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Main_future/.
scp -r LdF_West_current/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_West_current/.
scp -r LdF_West_future/data mnfienen@igsarmewfsM000.er.usgs.gov:LdF_West_future/.
scp LdF_Diff_OTB/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Diff_OTB/.
scp LdF_SE_OTB/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_SE_OTB/.
scp LdF_LGBK_OTB/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_LGBK_OTB/.
scp LdF_Main_current/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Main_current/.
scp LdF_Main_future/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_Main_future/.
scp LdF_West_current/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_West_current/.
scp LdF_West_future/worker.sh mnfienen@igsarmewfsM000.er.usgs.gov:LdF_West_future/.