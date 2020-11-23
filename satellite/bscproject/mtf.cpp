#include "encoder.h"

int main(){
    std::srand(1); //initialise PRNG with seed 1

    Simple8b d = Simple8b(3 ,"test.txt", 7000, "y", "None");
    d.loadData();

    d.genSamples(false);
    d.encodeData();
    
    return 0;
}
