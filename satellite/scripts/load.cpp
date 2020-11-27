#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>
#include "load.h"

void loop_through_vector(std::vector<int>& vec1);

int csv_load(std::string filePath, std::vector<std::vector<int>> &vecIn, int bits){

    double n;
    int count = 0;
    int remainder;

    std::vector<std::vector<int>> data{{},{},{}};

    std::ifstream infile;
    infile.open(filePath.c_str());

    if(!infile.is_open()){
        std::cout << "The file could not be opened" << std::endl;
        exit(EXIT_FAILURE);
    }

    while(infile >> n){
	if (count%4 != 0){
        	int vec_in = std::lround(n / 7.8125e-3);
		if (std::abs(vec_in) <  pow(2, bits)){ //change this to 16?
			data[count%4-1].push_back(vec_in); //i think this isn't working - maybe only taking one value
		}
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

int csv_save(std::string filePath, std::vector<float> vecIn){
	std::ofstream outf{filePath, std::ios::out};
	if (!outf){
		std::cerr << "Error opening file " << filePath << " !\n"; 
	}
	for (int i=0; i<vecIn.size(); i++){
		outf << vecIn[i] << "\n";
	}
	return 0;
}


int tolerances_save(std::string filePath, std::vector<std::vector<int>> vecIn){
	std::ofstream outf{filePath, std::ios::out};
	if (!outf){
		std::cerr << "Error opening file " << filePath << " !\n"; 
	}
	for (int i=0; i<vecIn.size(); i++){
		for (int j=0; j<vecIn[i].size(); j++){
			outf << vecIn[i][j] << " ";
		}
		outf << "\n";
	}
	return 0;
}



std::vector<std::string> generateFileList(std::string dirListFile){
	/*Given textfile with name of each file to be read on each line,
	get all these file names and return a vector of strings.*/
	std::vector<std::string> fileList;
	std::string n;
	std::ifstream infile;
    	infile.open(dirListFile);

	if(!infile){
		std::cout << "The file could not be opened" << std::endl;
        	exit(EXIT_FAILURE);
	}
	while (infile >> n){
		fileList.push_back(n);
	}
	return fileList;
}
