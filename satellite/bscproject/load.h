#ifndef LOAD_H
#define LOAD_H

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>

int csv_load(std::string filePath, std::string direction, std::vector<int> &vecIn);
<<<<<<< HEAD
=======
int csv_save(std::string filePath, std::vector<float> vecIn);
std::vector<std::string> generateFileList(std::string dirListFile);
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7

#endif
