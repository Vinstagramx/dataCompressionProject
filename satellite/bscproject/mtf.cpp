#include "encoder.h"

bool terminateEarly(std::vector<float> vecIn){
	/*Slice input vector of float compression ratios to 7 (can change this later) then check if each entry is less
	or same as previous and if it is return true. */
	bool earlyTerminate = false;
	if (vecIn.size() >= 7){
		std::vector<float> trimmedVec = std::vector<float>(vecIn.end()-7, vecIn.end()); 
		for (int i=1; i<trimmedVec.size(); i++){
			if (trimmedVec[i] <= trimmedVec[i-1]){
				earlyTerminate = false;
			}
		}
	}
	return earlyTerminate;
}

int main(){
	std::vector<std::string> filePaths = generateFileList("data/file_list.txt");
	std::vector<float> maxCompressionRatios;
	for (int file=0; file < filePaths.size(); file++){
		std::vector<float> compressionRatios;
		Delta d = Delta(3, filePaths[file], 7000, "y", "None");
		d.loadData();
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
	csv_save("data/test_save.txt", maxCompressionRatios);
    return 0;
}
