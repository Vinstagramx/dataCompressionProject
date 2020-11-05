#include "encoder.h"

int main(){
    Delta d = Delta(3 ,"test.txt", 7000, "y", "None");
    d.loadData();

    d.genSamples(false);
    d.encodeData();
    
    return 0;
}
