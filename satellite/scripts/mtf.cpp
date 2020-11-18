
#include "encoder.h"
#include <thread>
#include <future>
#include <chrono>
/* How to run the file:
	To input arguments use:
    $./mtf "Encoder type (Delta/Golomb)" "Sample Size" "Mode" "Outfile path" */
//Forward declaration of constants with some default params - overwritten by command line arguments
std::string ENC_TYPE = "Delta";
int SAMPLE_SIZE = 7000;
std::string MODE = "mean"; //can be "min" or "max"
std::string OUTFILE = "data/default.txt";

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

std::vector<float> split_mtf(std::vector<std::string> fileList){
    std::vector<float> maxCompressionRatios;
	std::string dirs[3] = {"x", "y", "z"};
	for (int file=0; file < fileList.size(); file++){
		Encoder temp = Encoder(3, fileList[file], SAMPLE_SIZE, "x", MODE);
		Encoder* d = temp.makeEncoder(ENC_TYPE);
		d->loadData();
		for(int j=0; j<3; j++){
			std::vector<float> compressionRatios;
			d->setDirection(dirs[j]);
			std::cout<< "file: " << fileList[file] << " in direction: " << dirs[j] << "\n";
			for (int i=3; i < 100; i++){
				d->setBlockSize(i);
				d->genSamples(false);
				d->encodeData();
				float compRat = d->getCompressionRatio();
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
    return maxCompressionRatios;
}

int main(int argc, char* argv[]){
	if (argc != 5){
		std::cout << "Please supply four command line arguments, encoder type, sample size, mode and outfile\n";
		exit(EXIT_FAILURE);
	}
	ENC_TYPE = argv[1];
	SAMPLE_SIZE = std::stoi(argv[2]);
	MODE = argv[3];
	OUTFILE = argv[4];
	auto start = std::chrono::high_resolution_clock::now();
	std::vector<std::string> filePaths = generateFileList("file_list.txt");
	std::vector<std::vector<std::string>> splitFilePaths{{}, {}, {}, {}};
	int listSize = filePaths.size();
	int divis = listSize/4; //four cores
	for (int i=0; i < 4; i++){ //split fileList into 4
        	std::vector<std::string> temp = std::vector<std::string>(filePaths.begin()+divis*i, filePaths.begin()+divis*(i+1));
        	splitFilePaths[i] = temp;
	}
	std::future<std::vector<float>> t1 = std::async(&split_mtf, splitFilePaths[0]);
	std::future<std::vector<float>> t2 = std::async(&split_mtf, splitFilePaths[1]);
	std::future<std::vector<float>> t3 = std::async(&split_mtf, splitFilePaths[2]);
	std::future<std::vector<float>> t4 = std::async(&split_mtf, splitFilePaths[3]);
	std::vector<float> compRat1 = t1.get();
	std::vector<float> compRat2 = t2.get();
	std::vector<float> compRat3 = t3.get();
	std::vector<float> compRat4 = t4.get();
	std::vector<std::vector<float>> combined{compRat1, compRat2, compRat3, compRat4};
	std::vector<float> maxCompressionRatios;
	for(int i=0; i<combined.size(); i++){
		for(int j=0; j <combined[i].size(); j++){
            		maxCompressionRatios.push_back(combined[i][j]);
        	}
    	}
	auto stop = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::minutes>(stop-start);
	std::cout << "finished successfully in " << duration.count() << " minutes \n";
	csv_save(OUTFILE, maxCompressionRatios);
	return 0;
}
