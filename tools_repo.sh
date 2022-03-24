#!/bin/bash


#gnu tools



#Frame
function download_FlameGraph()
{
    git clone git@github.com:brendangregg/FlameGraph.git
}


function download_gitgerrit()
{
    git clone git@github.com:deeperblue/git-gerrit.git
}



#### main ####
download_FlameGraph
download_gitgerrit







