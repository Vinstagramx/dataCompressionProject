#include "encoder.h"

int main(){
	std::vector<float> compressionRatios;
	Delta d = Delta(3 ,"data/test.txt", 7000, "y", "None");
	d.loadData();
	for (int i=3; i < 100; i++){
		d.genSamples(false);
		d.encodeData();
		float compRat = d.getCompressionRatio();
		compressionRatios.push_back(compRat);
	}
	csv_save("data/test_save.txt", compressionRatios);
    return 0;
}
