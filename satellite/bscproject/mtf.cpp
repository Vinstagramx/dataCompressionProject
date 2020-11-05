#include "encoder.h"

int main(){
    std::srand(1); //initialise PRNG with seed 1

    Delta d = Delta(3 ,"test.txt", 7000, "y", "None");
    d.loadData();

    d.genSamples(false);
    d.encodeData();
    
    return 0;
}
