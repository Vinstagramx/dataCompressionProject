#include "encoder.h"

int main(int argc, char* argv[]){
	std::string ENC_TYPE = argv[1];
	int SAMPLE_SIZE = std::stoi(argv[2]);
	std::string MODE = argv[3];
	std::string OUTFILE = argv[4];
	std::string FILELIST = argv[5];
	int BITS = std::stoi(argv[6]);
	std::vector<std::string> filePaths = generateFileList(FILELIST);
	std::string dirs[3] = {"x", "y", "z"};
	for (int fileIndex=0; fileIndex < filePaths.size(); fileIndex++){
		Encoder temp = Encoder(3, filePaths[fileIndex], SAMPLE_SIZE, "x", MODE, BITS);
		Encoder* d = temp.makeEncoder(ENC_TYPE);
		d->loadData();
		for (int j=0; j<3; j++){
			d->setDirection(dirs[j]);
			for (int i=21; i< 22; i++){
				d->setBlockSize(i);
				d->genSamples(false);
				d->encodeData(true);
			}
		}
	}
	return 0;
}
