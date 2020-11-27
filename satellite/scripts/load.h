#ifndef LOAD_H
#define LOAD_H

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>

int csv_load(std::string filePath,  std::vector<std::vector<int>> &vecIn, int bits);
int csv_save(std::string filePath, std::vector<float> vecIn);
int tolerances_save(std::string filePath, std::vector<std::vector<int>> vecIn);
std::vector<std::string> generateFileList(std::string dirListFile);

#endif
