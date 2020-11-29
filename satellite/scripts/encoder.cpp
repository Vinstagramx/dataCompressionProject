#include "encoder.h"
//TO DO - MAKE THE ENCODER TAKE SOME KINDA BIT LENGTH PARAMETER SO IT'S SUITABLE FOR MODIFIED DATA
	Encoder::Encoder(int bs=2, std::string f="test.txt", int samples=1000, std::string dir="x", std::string mode="None", int bits = 17){
		m_blockSize = bs;
		m_fileName = f;
		m_sampleNumber = samples;
		m_direction = dir;
		m_mode = mode;
		m_bits = bits;
	}
	
	Encoder *Encoder::makeEncoder(std::string choice){
		if (choice=="Delta"){
			return new Delta(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
		else if (choice=="Golomb"){
			return new Golomb(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
		else if (choice=="StepDelta"){
			return new StepDelta(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
		else if (choice == "Simple8b"){
			return new Simple8b(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
		else if (choice == "DeltaDelta"){
			return new DeltaDelta(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
		else{
			return new Encoder(m_blockSize, m_fileName, m_sampleNumber, m_direction, m_mode, m_bits);
		}
	}

	void Encoder::setBlockSize(int bs){ //can adjust blocksize inside object so don't need to load data multiple times
		m_blockSize = bs;
	}
	void Encoder::printParams(){ //debug function to check stuff is working
		std::cout << "block size: " << m_blockSize << " ";
		std::cout << "file: " << m_fileName << " ";
		std::cout << "sample number: " << m_sampleNumber << " ";
		std::cout << "direction: " << m_direction <<" ";
		std::cout << "mode: " << m_mode << " ";
		std::cout << "bit length " << m_bits << "\n";
	}

	void Encoder::setDirection(std::string dir){
		/*To let you adjust the directional data as you go so you call load data less*/
		m_direction = dir;
		if (m_direction == "x"){
			m_data = m_allData[0];
		}
		if (m_direction == "y"){
			m_data = m_allData[1];
		}
		if (m_direction == "z"){
			m_data = m_allData[2];
		}
		//std::cout << "first value in " << m_direction << "is:" << m_data[0] << "\n";
	}

	void Encoder::loadData(){
		csv_load(m_fileName, m_allData, m_bits); //return by reference to load data into m_data
		std::cout << "loaded data succesfully \n";
		setDirection(m_direction); //set data to be whichever direction we initialised the class with
	}

	void Encoder::printData(){ //debug to check stuff is working
		for (int i = 0; i < m_data.size(); i++){
			std::cout << m_data[i] << "\n";
		}
	}

	float Encoder::getCompressionRatio(){
		return m_compressionRatio;
	}
	
	int Encoder::getDataLength(){
		return m_data.size();
	}

	void Encoder::genSamples(bool random){
		/*Create list of indices spaced by blocksize from which m_sampleIndices are selected and returned using PRNG*/
		int maxSampleIndex = m_data.size()/m_blockSize;
		for (int i = 0; i < maxSampleIndex; i++){
			m_sampleIndices.push_back(i*m_blockSize);
		}
		std::srand(1); //initialise PRNG with seed 1
		std::random_shuffle (m_sampleIndices.begin(), m_sampleIndices.end()); //shuffling then erasing all indices past the sample number required is same as random selection without replacement
		m_sampleIndices.erase(m_sampleIndices.begin()+m_sampleNumber, m_sampleIndices.end());
		//std::cout <<"sample indices is length " << m_sampleIndices.size() << "\n";
	}

	Encoded Encoder::encode(std::vector<int> &block){ //method to be overwritten by specific encoding schemes later
		Encoded encodedBlock;
		encodedBlock.codewords = std::vector<int>{0}; //initialise this way to avoid seg fault
		encodedBlock.encodedData = std::vector<std::vector<int>>{block}; //ditto
		return encodedBlock;
	}

	std::string Encoder::binaryString(int n){
		/*Return the smallest binary representation of a given integer n with added sign bit at the end*/
		char signBit = '0';
		if (n < 0){
			signBit = '1';
		}
		int a = std::abs(n);
		std::string truncated;
		if (a == 0){ //otherwise i will exceed range and cause seg fault
			truncated = "0";
		}
		else{ //could improve this with recursive definition on stack overflow
			std::string binary = std::bitset<18>(a).to_string();//maximum representable measurement is 14 bits
			int loop = 0; //change 14/16 bits ? weird seg fault
			while (binary[loop] != '1'){ //if 0 then is not significant bit
				++loop;
				}
			truncated = binary.substr(loop); //creates substring from position loop until end
		}
		truncated.insert(truncated.begin(), signBit); //add sign bit
		return truncated;
	}

	int Encoder::calcBitLength(Encoded encBlock){
		/*Calculate the bit length in an encoded block. First coverts list of codewords into bit lengths
		then loops through every block of encoded data (can be more than 1 for golomb), calculates the bit
		lengths of every element then multiplies the longest bit length by the block size to get the 
		compressed bit length for that block. Sum these block bit lengths together and add codeword length
		then return.*/
		int codewordLength = 0;
		for (int i=0; i < encBlock.codewords.size(); i++){ //for each codeword in codewords
			int binLength = binaryString(encBlock.codewords[i]).length(); //get length of binary string of codeword
			codewordLength += binLength;
		}
		int blockLength = 0;
		for (int i=0; i < encBlock.encodedData.size(); i++){ //for each block in encoded data
			std::vector<int> bitLengths; //maybe optimise later by setting this to size of encodedData.size() and using indexing rather than push_back
			for (int j=0; j < encBlock.encodedData[i].size(); j++){ //for each integer in block
				int binLength = binaryString(encBlock.encodedData[i][j]).length();
				bitLengths.push_back(binLength);
			}
			int maxVal = *std::max_element(bitLengths.begin(), bitLengths.end()); //use * as std::max_element returns iterator
			blockLength += maxVal * encBlock.encodedData[i].size(); //block bit length should be the length of longest bit * size of block (implict truncation)
		}
		int sum = codewordLength + blockLength;
		return sum;
	}

	int Encoder::encodeData(bool decodeFlag=false){
		/*Big method to handle generic encoding process for the data*/
		int uncompressedBitLength = 0; //total bit length of uncompressed data
		float compressedBitLength = 0; //total bit length of compressed data, is float so division later returns float
		for (int i=0; i < m_sampleIndices.size(); i++){ //for each sample
			int sampleIndex = m_sampleIndices[i];
			std::vector<int> block;
			Encoded encodedBlock;
			block = std::vector<int>(m_data.begin() + sampleIndex, m_data.begin() + sampleIndex + m_blockSize); //use vector copy constructor to slice m_data and assign to block
			encodedBlock = encode(block);

			uncompressedBitLength += m_bits*m_blockSize; //assumes unencoded block are all 14 bit numbers 
			int encodedBlockBitLength = calcBitLength(encodedBlock);
			if (encodedBlockBitLength > m_bits*m_blockSize){ //equivalent to unencoded flag in paper, i.e if encoded block is somehow BIGGER than unencoded, transmit unencoded
				compressedBitLength += m_bits*m_blockSize;
			}
			else{
				compressedBitLength += encodedBlockBitLength;
			}
			if (decodeFlag==true){
				std::vector<int> decodedBlock = decode(encodedBlock);
				for (int i=0; i<decodedBlock.size(); i++){
					std::cout<< "dec block: " << decodedBlock[i] << " , orig block: " << block[i] << "\n";
					if (decodedBlock[i] != block[i]){
						std::cout << "Error, orignal and decoded block don't match \n";
					}
				}
			}
		}
		float compressionRatio = (1- compressedBitLength/uncompressedBitLength)*100;
		//std::cout << m_direction << " space saving ratio is: " << compressionRatio << "\n";
		m_compressionRatio = compressionRatio;
		return 0;
	}

	std::vector<int> Encoder::decode(Encoded encodedBlock){
		/*Generic method to overwrite later*/
		std::vector<int> decoded = encodedBlock.encodedData[0];
		return decoded;
	}


	Encoded Delta::encode(std::vector<int> &block){
		/*Overwrite the encode method with delta specific implementation - subtract each element
		from the previous element then return the encoded block.*/
		int codeword = block[0];
		Encoded encodedBlock;
		std::vector<int> encodedVec;
		//encodedVec.push_back(0); //first value should be 0 as difference from codeword
		for (int i=1; i<block.size()-1; i++){
			encodedVec.push_back(block[i]-block[i-1]);
		}
		encodedBlock.codewords = std::vector<int>{codeword};
		encodedBlock.encodedData = std::vector<std::vector<int>>{encodedVec};
		return encodedBlock;
	}

	std::vector<int> Delta::decode(Encoded encodedBlock){
		/*Decode the encoded block by performing reverse delta process - take codeword then add it to first value
		then add prev value of decoded block to each value of encoded block.*/
		std::vector<int> encBlock = encodedBlock.encodedData[0];
		std::vector<int> decodedBlock;
		int codeword = encodedBlock.codewords[0];
		int firstValue = codeword;
		decodedBlock.push_back(firstValue);
		for (int i=1; i<encBlock.size()-1; i++){
			decodedBlock.push_back(encBlock[i-1]+decodedBlock[i-1]); //i think enc block doesn't have 0 as first value
		}
		return decodedBlock;
	}

	std::string Golomb::unary(int n){
		std::string unaryString = "0";
		uint absN = std::abs(n);
		for (int i=0; i < absN; i++){
			unaryString.insert(unaryString.begin(),'1');
		}
		//std::cout << "n is: " << n << " and unary is: " << unaryString < "\n";
		return unaryString;
	}

	Encoded Golomb::encode(std::vector<int> &block){
		/*Overwrite the encode method with Golomb specific implementation - divide each number
		in block by fixed paramter b which is determined by the mode. Store the quotient q in
		unary in one block of instance of Encoded and the remainders in another.*/
		Encoded encodedBlock;
		int b = 0;
		std::vector<int> absBlock;
		for (int i=0; i< block.size(); i++){
			absBlock.push_back(std::abs(block[i])); //need block of only +ve values to find max and min of 
		}

		if (m_mode == "mean"){
			float average = std::accumulate(block.begin(), block.end(), 0.0)/block.size(); //find the average using acucmulate
			b = std::round(average); //need b to be int for golomb to work
		} else if (m_mode == "min"){
			b = *std::min_element(absBlock.begin(), absBlock.end());
		} else if (m_mode == "max"){
			b = *std::max_element(absBlock.begin(), absBlock.end());
		}

		std::vector<int> remainderBlock;
		std::vector<int> quotientBlock;
		for (int n=0; n< block.size(); n++){
			int absN = std::abs(block[n]); //need absolute value for consistency between -ve and +ve
			int q = (b == 0) ? 0 : absN/b; //check here, but should be integer division that rounds down/discards decimal part 
			int r = 0;
			if (n < 0){
				r = block[n] + q*b;
			}
			else{
				r = block[n] - q*b;
			}
			remainderBlock.push_back(r);
			quotientBlock.push_back(q);
		}
		encodedBlock.codewords.push_back(b);
		encodedBlock.encodedData.push_back(quotientBlock);
		encodedBlock.encodedData.push_back(remainderBlock);
		return encodedBlock;
	}

	std::vector<int> Golomb::decode(Encoded encodedBlock){
		int b = encodedBlock.codewords[0];
		std::vector<int> quotientBlock = encodedBlock.encodedData[0];
		std::vector<int> remainderBlock = encodedBlock.encodedData[1];
		std::vector<int> decodedBlock;
		for (int i=0; i<quotientBlock.size(); i++){
			int r = remainderBlock[i];
			int q = quotientBlock[i];
			int n;
			if (r>0){
				n = r+q*b;
			}
			else{
				n = r-q*b;
			}
			decodedBlock.push_back(n);
		}
		return decodedBlock;
	}

	int Golomb::calcBitLength(Encoded encBlock){
		/*Overwritten for golomb because the first block in encoded data needs to be encoded in unary, the rest in binary*/
		int codewordLength = 0;
		for (int i=0; i < encBlock.codewords.size(); i++){ //for each codeword in codewords
			int binLength = binaryString(encBlock.codewords[i]).length(); //get length of binary string of codeword
			codewordLength += binLength;
		}
		int blockLength = 0;
		std::vector<int> unaryBitLengths;
		for (int i=0; i < encBlock.encodedData[0].size(); i++){ //assuming the first block is the quotient block to be encoded in unary
			int unaryLength = unary(encBlock.encodedData[0][i]).length();
			unaryBitLengths.push_back(unaryLength);
		}
		int maxUnaryVal =  *std::max_element(unaryBitLengths.begin(), unaryBitLengths.end());
		blockLength += maxUnaryVal*m_blockSize;

		for (int i=1; i < encBlock.encodedData.size(); i++){ //for each other block in encoded data
			std::vector<int> bitLengths; //maybe optimise later by setting this to size of encodedData.size() and using indexing rather than push_back
			for (int j=0; j < encBlock.encodedData[i].size(); j++){ //for each integer in block
				int binLength = binaryString(encBlock.encodedData[i][j]).length();
				bitLengths.push_back(binLength);
			}
			int maxVal = *std::max_element(bitLengths.begin(), bitLengths.end()); //use * as std::max_element returns iterator
			blockLength += maxVal * encBlock.encodedData[i].size(); //block bit length should be the length of longest bit * size of block (implict truncation)
		}
		int sum = codewordLength + blockLength;
		return sum;
	}

	Encoded StepDelta::encode(std::vector<int> &block){
		/*Define a filter value. Then loop through the block until there's a big jump. Determine the direction and 
		that sets which one is the high stream codeword & initial value, and which is the low stream codeword and 
		initial value. Then loop through and encode by checking if there's a jump then switching to high or low
		stream and subtracting the previous value in that high or low stream. Note that this might reduce performance by 
		more than expected as i've effectively increased the time between samples by splitting (so more oppurtunity for 
		variance into two streams*/
		//float filter = 3/7.8125e-3; //a jump of 3nT in scaled units
		float filter = *std::max_element(block.begin(), block.end())/2;//std::accumulate(block.begin(), block.end(), 0.0)/block.size(); //find the average using acucmulate
		int smallCodeword = block[0];
		int bigCodeword = block[0];
		for (int i=0; i <block.size(); i++){
			if (block[i] < filter){
				smallCodeword = block[i];
			}
			break;
		}
		for (int i=0; i <block.size(); i++){
			if (block[i] > filter){
				bigCodeword = block[i];
			}
			break;
		}
		//need some way of ensuring one value is the lower and the other 
		int lastBig = bigCodeword;
		int lastSmall = smallCodeword;
		Encoded encodedBlock;
		std::vector<int> encodedVec;
		std::vector<int> flagVec;
		 //set this in the initial sweep
		//encodedVec.push_back(0); //first value should be 0 as difference from codeword
		for (int i=0; i<block.size(); i++){
			if (block[i]<filter){
				encodedVec.push_back(block[i]-lastSmall);
				lastSmall = block[i];
				//lastBig = block[i-1];
				flagVec.push_back(0);
			}
			else{
				encodedVec.push_back(block[i]-lastBig);
				//lastSmall = block[i-1];
				lastBig = block[i];
				flagVec.push_back(1);
			}
		}
		encodedBlock.codewords = std::vector<int>{smallCodeword, bigCodeword};
		encodedBlock.encodedData = std::vector<std::vector<int>>{flagVec, encodedVec};
		return encodedBlock;

	}

	int StepDelta::calcBitLength(Encoded encBlock){
		int codewordLength = 0;
		for (int i=0; i < encBlock.codewords.size(); i++){ //for each codeword in codewords
			int binLength = binaryString(encBlock.codewords[i]).length(); //get length of binary string of codeword
			codewordLength += binLength;
		}
		int blockLength = 0;
		std::vector<int> unaryBitLengths;
		for (int i=0; i < encBlock.encodedData[0].size(); i++){ //assuming the first block is the quotient block to be encoded in unary
			int unaryLength = 1;
			unaryBitLengths.push_back(unaryLength);
		}
		//int maxUnaryVal =  *std::max_element(unaryBitLengths.begin(), unaryBitLengths.end());
		blockLength += encBlock.encodedData[0].size();

		for (int i=1; i < encBlock.encodedData.size(); i++){ //for each other block in encoded data
			std::vector<int> bitLengths; //maybe optimise later by setting this to size of encodedData.size() and using indexing rather than push_back
			for (int j=0; j < encBlock.encodedData[i].size(); j++){ //for each integer in block
				int binLength = binaryString(encBlock.encodedData[i][j]).length();
				bitLengths.push_back(binLength);
			}
			int maxVal = *std::max_element(bitLengths.begin(), bitLengths.end()); //use * as std::max_element returns iterator
			blockLength += maxVal * encBlock.encodedData[i].size(); //block bit length should be the length of longest bit * size of block (implict truncation)
		}
		int sum = codewordLength + blockLength;
		return sum;
	}

	Encoded Simple8b::encode(std::vector<int> &block){
		/* Simple-8b algorithm. Encoded data returned in the form of a vector of codewords (from the prerequisite delta encoding),
		a vector of selectors, and a vector of encoded integers. Bit lengths of these three separate components would then need to be calculated
		in the calcBitLength function. Note each 'block' of data from the simple-8b algorithm contains the selector (4 bits) and the payload (encoded data - 60 bits)*/
		int codeword = block[0];
		// std::cout << "codeword" << codeword << std::endl;
		Encoded encodedBlock;
		std::vector<int> encodedVec;  // Vector which houses result of delta encoding scheme
		//encodedVec.push_back(0); //first value should be 0 as difference from codeword
		for (int i=1; i < block.size(); i++){ // Delta Encoding
			encodedVec.push_back(block[i]-block[i-1]);
			// std::cout << encodedVec[i-1] << std::endl;
		}
		encodedBlock.codewords.push_back(codeword);  // Returning codeword as part of encodedBlock
		int cumBits;
		int ind = 0;  // Index of previously full 64-bit block (initialised at 0)
		std::vector<int> encodedSubBlock;  // Sub-blocks of data - reset every time the payload is filled
		for (int j=0; j < encodedVec.size(); j++){ //for each integer in delta vector
			std::vector<int> tempVec; // Temporary vector - for the purpose of finding the cumulative bit length
			std::vector<int> tempLengthsVec; // Bit lengths of temporary vector - used to find the selector.
			if (j == ind){
				continue;
			}
			else{
				for (int k = ind; k < j; k++){  // From index of previous full payload to current index
					// std::cout << encodedVec[k] << std::endl;
					tempVec.push_back(encodedVec[k]);
					tempLengthsVec.push_back(binaryString(encodedVec[k]).length());
				}
			}
			
			cumBits = calcCumBitLength(tempVec);
			int nextBits;
			if (j != encodedVec.size() - 1){
				nextBits = cumBits + binaryString(encodedVec[j+1]).length(); // Cumulative bits at current index + bit length of next datapoint
				// std::cout << "nextbits = " << nextBits << std::endl;
			}

			if(nextBits > 60){
				int maxVal = *std::max_element(tempLengthsVec.begin(), tempLengthsVec.end()); //use * as std::max_element returns iterator
				int selector = findSelector(maxVal);
				encodedBlock.codewords.push_back(selector); // Find corresponding selector to max bit length datapoint.
				encodedSubBlock.clear();  // Clears previous entries of sub-block
				for (int l = ind; l < j; l++){
					// std::cout << l << std::endl;
					encodedSubBlock.push_back(encodedVec[l]); // need to add padding
				}
				encodedBlock.encodedData.push_back(encodedSubBlock);  // Return encoded
				ind = j+1; // Start a new 64-bit block, and the payload searching process, from the next index.
			}		
			if(j == encodedVec.size() - 1){ // If end of block is reached without payload is full (less than 60 bits), need to pad with zeros and push back.
				int maxVal = *std::max_element(tempLengthsVec.begin(), tempLengthsVec.end()); //use * as std::max_element returns iterator
				int selector = findSelector(maxVal);
				encodedBlock.codewords.push_back(selector); // Find corresponding selector to max bit length datapoint.
				encodedSubBlock.clear();  // Clears previous entries of sub-block
				for (int l = ind; l < j; l++){
					// std::cout << "End of block, index = " << l << std::endl;
					encodedSubBlock.push_back(encodedVec[l]); // need to add padding
				}
				encodedBlock.encodedData.push_back(encodedSubBlock);  // Return encoded
			}
		}
		return encodedBlock;
	}

	int Simple8b::findSelector(int bitLength){
		/* Finds the selector of the simple-8b algorithm based on the number of bits needed to represent a given number */
		int selector;
		if(bitLength <= 8){
			selector = bitLength + 1;
		}
		else if(bitLength > 8 && bitLength <= 10){
			selector = 10;
		}
		else if(bitLength > 10 && bitLength <= 12){
			selector = 11;
		}
		else if(bitLength > 12 && bitLength <= 15){
			selector = 12;
		}		
		else if(bitLength > 15 && bitLength <= 20){
			selector = 13;
		}
		else if(bitLength > 20 && bitLength <= 30){
			selector = 14;
		}		
		else if(bitLength > 30 && bitLength <= 60){
			selector = 15;
		}		
		return selector;
	}

	int Simple8b::bitLengthRound(int bitLength){
		/* Rounds the bit length to the next width as determined by the selector */
		int round;
		if(bitLength > 8 && bitLength <= 10){
			round = 10;
		}
		else if(bitLength > 10 && bitLength <= 12){
			round = 12;
		}
		else if(bitLength > 12 && bitLength <= 15){
			round = 15;
		}		
		else if(bitLength > 15 && bitLength <= 20){
			round = 20;
		}
		else if(bitLength > 20 && bitLength <= 30){
			round = 30;
		}		
		else if(bitLength > 30 && bitLength <= 60){
			round = 60;
		}
		else{
			round = bitLength;
		}
		return round;
	}

	int Simple8b::calcCumBitLength(std::vector<int> deltaVec){
		/*Overwritten for Simple-8b: we need the cumulative bit length as we add more points to the payload*/
		int blockLength = 0;
		std::vector<int> bitLengths;
		for (int i=0; i < deltaVec.size(); i++){ //for each block in encoded data
			int binLength = binaryString(deltaVec[i]).length();
			bitLengths.push_back(binLength);
		}
		int maxVal = *std::max_element(bitLengths.begin(), bitLengths.end()); //use * as std::max_element returns iterator
		maxVal = bitLengthRound(maxVal); // Rounding the bit length to the next available width as determined by the selector
		blockLength += maxVal*deltaVec.size(); //block bit length should be the length of longest bit * size of block (implict truncation)
		return blockLength;
	}

	int Simple8b::calcBitLength(Encoded encBlock){
		/*Overwritten for Simple-8b, as we need to find the bit lengths of the codewords, selectors, and the data in the block */
		int codewordLength = 0;
		codewordLength += binaryString(encBlock.codewords[0]).length(); //get length of binary string of codeword
		for (int i=1; i < encBlock.codewords.size(); i++){ //for each selector in codewords
			codewordLength += 4;
		}

		int blockLength = 0;
		for (int i=0; i < encBlock.encodedData.size(); i++){ //for each other block in encoded data
		std::vector<int> bitLengths; //maybe optimise later by setting this to size of encodedData.size() and using indexing rather than push_back
			for (int j=0; j < encBlock.encodedData[i].size(); j++){ //for each sub-block in block
				// int binLength = binaryString(encBlock.encodedData[i][j]).length();  // For each val in sub-block
				// bitLengths.push_back(binLength);
				blockLength += 60;
			}

		}
		
		int sum = codewordLength + blockLength;
		return sum;
	}

	Encoded DeltaDelta::encode(std::vector<int> &block){
		/*Overwrite the encode method with delta-of-delta specific implementation - subtract each element
		from the previous element then return the encoded block. Repeat this procedure again.*/
		int codeword = block[0];
		Encoded encodedBlock;
		std::vector<int> encodedVec;
		std::vector<int> codewords;
		std::vector<int> encodedDeltaVec;
		//encodedVec.push_back(0); //first value should be 0 as difference from codeword
		for (int i=1; i<block.size()-1; i++){
			encodedVec.push_back(block[i]-block[i-1]);
		}
		codewords.push_back(codeword);
		codewords.push_back(encodedVec[0]);
		for (int j=1; j < encodedVec.size()-1; j++){
			encodedDeltaVec.push_back(encodedVec[j]-encodedVec[j-1]);
		}
		encodedBlock.codewords = codewords;
		encodedBlock.encodedData = std::vector<std::vector<int>>{encodedDeltaVec};
		return encodedBlock;
	}

	std::vector<int> DeltaDelta::decode(Encoded encodedBlock){
		/*Decode the encoded block by performing reverse delta process - take codeword then add it to first value
		then add prev value of decoded block to each value of encoded block.*/
		std::vector<int> encBlock = encodedBlock.encodedData[0];
		std::vector<int> decodedBlock;
		int codeword = encodedBlock.codewords[0];
		int deltaCodeword = encodedBlock.codewords[1];
		int firstValue = codeword;
		int secondValue = deltaCodeword;
		decodedBlock.push_back(firstValue);
		decodedBlock.push_back(secondValue);
		for (int i=2; i < encBlock.size()-1; i++){
			decodedBlock.push_back(encBlock[i-1]+decodedBlock[i-1]); //i think enc block doesn't have 0 as first value
		}
		return decodedBlock;
	}
	
    Encoded DeltaGolomb::encode(std::vector<int> &block){
		/*Overwrite the encode method with Golomb specific implementation - divide each number
		in block by fixed paramter b which is determined by the mode. Store the quotient q in
		unary in one block of instance of Encoded and the remainders in another.*/
		Encoded encodedBlock;
		int b = 0;
		std::vector<int> absBlock;
		for (int i=0; i< block.size(); i++){
			absBlock.push_back(std::abs(block[i])); //need block of only +ve values to find max and min of 
		}

		if (m_mode == "mean"){
			float average = std::accumulate(block.begin(), block.end(), 0.0)/block.size(); //find the average using acucmulate
			b = std::round(average); //need b to be int for golomb to work
		} else if (m_mode == "min"){
			b = *std::min_element(absBlock.begin(), absBlock.end());
		} else if (m_mode == "max"){
			b = *std::max_element(absBlock.begin(), absBlock.end());
		}

		std::vector<int> deltaBlock;
		int deltaCodeword = block[0];
		//deltaBlock.push_back(deltaCodeword)
		for (int n=1; n<block.size()-1; n++){
			deltaBlock.push_back(block[n]-block[n-1]);
		}
		
		std::vector<int> remainderBlock;
		std::vector<int> quotientBlock;
		for (int n=0; n< deltaBlock.size(); n++){
			int absN = std::abs(deltaBlock[n]); //need absolute value for consistency between -ve and +ve
			int q = (b == 0) ? 0 : absN/b; //check here, but should be integer division that rounds down/discards decimal part 
			int r = 0;
			if (deltaBlock[n] < 0){
				r = deltaBlock[n] + q*b;
			}
			else{
				r = deltaBlock[n] - q*b;
			}
			remainderBlock.push_back(r);
			quotientBlock.push_back(q);
		}
		encodedBlock.codewords.push_back(deltaCodeword);
		encodedBlock.codewords.push_back(b);
		encodedBlock.encodedData.push_back(quotientBlock);
		encodedBlock.encodedData.push_back(remainderBlock);
		return encodedBlock;
	}
