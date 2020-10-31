#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>
#include "load.h"

void loop_through_vector(std::vector<int>& vec1);

int csv_load(std::string filePath, std::string direction, std::vector<int> &vecIn){

    double n;
    int count = 0;
    int remainder;

    std::vector<int> data;

    std::ifstream infile;
    infile.open(filePath.c_str());

    if(!infile.is_open()){
        std::cout << "The file could not be opened" << std::endl;
        exit(EXIT_FAILURE);
    }

    if(direction == "x"){
        remainder = 1;
    }
    else if (direction == "y"){
        remainder = 2;
    }
    else if (direction == "z"){
        remainder = 3;
    }

    while(infile >> n){
        if(count % 4 == remainder){
            int vec_in = std::lround(n / 7.8125e-3);
            data.push_back(vec_in);
        }
        count++;
    }
    vecIn = data;
    return 0;
}

void loop_through_vector(std::vector<int>& vec1){
    for(int i = 0; i < vec1.size(); i++){
        std::cout << vec1[i] << " \n";
    }

}

