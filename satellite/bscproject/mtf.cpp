#include "encoder.h"
#include <chrono>

bool terminateEarly(std::vector<float> vecIn){
	/*Slice input vector of float compression ratios to 7 (can change this later) then check if each entry is less
	or same as previous and if it is return true. */
	bool earlyTerminate = false;
	if (vecIn.size() >= 3){
		std::vector<float> trimmedVec = std::vector<float>(vecIn.end()-2, vecIn.end()); 
		for (int i=1; i<trimmedVec.size(); i++){
			if (trimmedVec[i] <= trimmedVec[i-1]){
				earlyTerminate = false;
			}
		}
	}
	return earlyTerminate;
}

int main(){
	auto start = std::chrono::high_resolution_clock::now();
	std::vector<std::string> filePaths = generateFileList("data/file_list.txt");
	std::vector<float> maxCompressionRatios;
	std::string dirs[3] = {"x", "y", "z"};
	for (int file=0; file < filePaths.size(); file++){
		std::vector<float> compressionRatios;
		Delta d = Delta(3, filePaths[file], 7000, "x", "None");
		d.loadData();
		for(int j=0; j<3; j++){
			d.setDirection(dirs[j]);
			std::cout<< "file: " << filePaths[file] << " in direction: " << dirs[j] << "\n";
			for (int i=3; i < 100; i++){
				d.setBlockSize(i);
				d.genSamples(false);
				d.encodeData();
				float compRat = d.getCompressionRatio();
				compressionRatios.push_back(compRat);
				if (terminateEarly(compressionRatios)){
					std::cout << "local max found, terminating \n";
					break;
				}
			}
			float max = *std::max_element(compressionRatios.begin(), compressionRatios.end());
			maxCompressionRatios.push_back(max);
			}
		}
	auto stop = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::minutes>(stop-start);
	std::cout << "finished successfully in " << duration.count() << " minutes";
	csv_save("data/test_save.txt", maxCompressionRatios);
    return 0;
}
