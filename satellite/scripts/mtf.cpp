
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
std::string FILELIST = "file_list.txt";
int BITS = 14;
std::string TOLERANCE = "False";

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

std::vector<std::vector<std::vector<float>>> split_mtf(std::vector<std::string> fileList){
	std::vector<std::vector<std::vector<float>>> fileCompressionRatios;
	std::string dirs[3] = {"x", "y", "z"};
	for (int file=0; file < fileList.size(); file++){
		Encoder temp = Encoder(5, fileList[file], SAMPLE_SIZE, "x", MODE, BITS);
		Encoder* d = temp.makeEncoder(ENC_TYPE);
		d->loadData();
		std::vector<std::vector<float>> directionCompressionRatios;
		for(int j=0; j<3; j++){
			std::vector<float> compressionRatios;
			d->setDirection(dirs[j]);
			std::cout<< "file: " << fileList[file] << " in direction: " << dirs[j] << "\n";
			for (int i=3; i < 100; i++){
				d->setBlockSize(i);
				d->genSamples(false);
				d->encodeData(false);
				float compRat = d->getCompressionRatio();
				compressionRatios.push_back(compRat);
				if (terminateEarly(compressionRatios)){
					std::cout << "local max found, terminating \n";
					break;
				}
			}
			//float max = *std::max_element(compressionRatios.begin(), compressionRatios.end());
			directionCompressionRatios.push_back(compressionRatios);
			}
	fileCompressionRatios.push_back(directionCompressionRatios);
	}
    return fileCompressionRatios;
}

int main(int argc, char* argv[]){
	if (argc != 8){
		std::cout << "Please supply six command line arguments, encoder type, sample size, mode, outfile, file list, and bit length\n";
		exit(EXIT_FAILURE);
	}
	ENC_TYPE = argv[1];
	SAMPLE_SIZE = std::stoi(argv[2]);
	MODE = argv[3];
	OUTFILE = argv[4];
	FILELIST = argv[5];
	BITS = std::stoi(argv[6]);
	TOLERANCE = argv[7];
	auto start = std::chrono::high_resolution_clock::now();
	std::vector<std::string> filePaths = generateFileList(FILELIST);
	std::vector<std::vector<std::string>> splitFilePaths{{}, {}, {}, {}};
	int listSize = filePaths.size();
	int divis = listSize/4; //four cores
	for (int i=0; i < 4; i++){ //split fileList into 4
        	std::vector<std::string> temp = std::vector<std::string>(filePaths.begin()+divis*i, filePaths.begin()+divis*(i+1));
        	splitFilePaths[i] = temp;
	}
	/*So not sure the best way to get two things out of async so what I did was just return an 3xN array of all the compression ratios
	we got from t1, t2, etc. This means we need to do some ugly array parsing to get the max data out but it also means we can get
	the tolerance in the same way.*/
	auto t1 = std::async(&split_mtf, splitFilePaths[0]);
	auto t2 = std::async(&split_mtf, splitFilePaths[1]);
	auto t3 = std::async(&split_mtf, splitFilePaths[2]);
	auto t4 = std::async(&split_mtf, splitFilePaths[3]);
	auto compRat1 = t1.get();
	auto compRat2 = t2.get();
	auto compRat3 = t3.get();
	auto compRat4 = t4.get();
	std::vector<std::vector<std::vector<std::vector<float>>>> combined{compRat1, compRat2, compRat3, compRat4};
	std::vector<float> maxCompressionRatios;
	std::vector<std::vector<int>> tolerances;
	for(int i=0; i<combined.size(); i++){
		for(int j=0; j <combined[i].size(); j++){
			for (int k=0; k<combined[i][j].size(); k++){
				float max = *std::max_element(combined[i][j][k].begin(), combined[i][j][k].end());
				if (TOLERANCE=="True"){
					std::vector<int> tempTolerances;
					std::vector<float> dirCompRat = combined[i][j][k];
					for (int m=0; m<dirCompRat.size(); m++){
						if (dirCompRat[m] >= 0.95*max) { //check if these directional compression ratios are within 95% of max
							tempTolerances.push_back(m);
						}
					}
					if (!tempTolerances.empty()){
						std::vector<int> tempMaxMin{tempTolerances.front(), tempTolerances.back()}; //a tuple of first and last values - the range of the tolerance
						tolerances.push_back(tempMaxMin);
					}
					else{
						std::vector<int> tempMaxMin{0, 0};
						tolerances.push_back(tempMaxMin);
					}
				}
				maxCompressionRatios.push_back(max);
			}
		}
	}
	auto stop = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::minutes>(stop-start);
	std::cout << "finished successfully in " << duration.count() << " minutes \n";
	csv_save(OUTFILE, maxCompressionRatios);
	if (TOLERANCE == "True"){
		tolerances_save("tolerances.txt", tolerances);
	}
	return 0;
}
