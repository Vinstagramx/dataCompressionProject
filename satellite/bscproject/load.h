#ifndef LOAD_H
#define LOAD_H

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>

int csv_load(std::string filePath, std::string direction, std::vector<int> &vecIn);
int csv_save(std::string filePath, std::vector<float> vecIn);

#endif
