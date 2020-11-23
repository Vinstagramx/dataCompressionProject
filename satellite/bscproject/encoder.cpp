#include "encoder.h"


  //  Encoder::Encoder(){ //default constructor
//		m_blockSize = 2;
//		m_fileName = "test.txt";
//		m_sampleNumber = 1000;
//		m_direction = "x";
	//	m_mode = "None";
	//}
	Encoder::Encoder(int bs=2, std::string f="test.txt", int samples=1000, std::string dir="x", std::string mode="None"){
        m_blockSize = bs;
		m_fileName = f;
		m_sampleNumber = samples;
		m_direction = dir;
		m_mode = mode;
	}
	void Encoder::setBlockSize(int bs){ //can adjust blocksize inside object so don't need to load data multiple times
		m_blockSize = bs;
	}
	void Encoder::printParams(){ //debug function to check stuff is working
		std::cout << "block size: " << m_blockSize << " ";
		std::cout << "file: " << m_fileName << " ";
		std::cout << "sample number: " << m_sampleNumber << " ";
		std::cout << "direction: " << m_direction <<"\n";
	}
	void Encoder::loadData(){
		csv_load(m_fileName, m_direction, m_data); //return by reference to load data into m_data
		std::cout << "loaded data succesfully \n";
	}
	void Encoder::printData(){ //debug to check stuff is working
		for (int i = 0; i < m_data.size(); i++){
			std::cout << m_data[i] << "\n";
		}
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
			std::string binary = std::bitset<14>(a).to_string();//maximum representable measurement is 14 bits
			int loop = 0;
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
			blockLength += maxVal*m_blockSize; //block bit length should be the length of longest bit * size of block (implict truncation)
		}
		int sum = codewordLength + blockLength;
		return sum;
	}

	int Encoder::encodeData(){
		/*Big method to handle generic encoding process for the data*/
		int uncompressedBitLength = 0; //total bit length of uncompressed data
		float compressedBitLength = 0; //total bit length of compressed data, is float so division later returns float
		for (int i=0; i < m_sampleIndices.size(); i++){ //for each sample
			int sampleIndex = m_sampleIndices[i];
			std::vector<int> block;
			Encoded encodedBlock;
			block = std::vector<int>(m_data.begin() + sampleIndex, m_data.begin() + sampleIndex + m_blockSize); //use vector copy constructor to slice m_data and assign to block
			encodedBlock = encode(block);

			uncompressedBitLength += 14*m_blockSize; //assumes unencoded block are all 14 bit numbers 
			int encodedBlockBitLength = calcBitLength(encodedBlock);
			if (encodedBlockBitLength > 14*m_blockSize){ //equivalent to unencoded flag in paper, i.e if encoded block is somehow BIGGER than unencoded, transmit unencoded
				compressedBitLength += 14*m_blockSize;
			}
			else{
				compressedBitLength += encodedBlockBitLength;
			}
		}
		float compressionRatio = (1- compressedBitLength/uncompressedBitLength)*100;
		std::cout << m_direction << " space saving ratio is: " << compressionRatio << "\n";
		return 0;
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
			blockLength += maxVal*m_blockSize; //block bit length should be the length of longest bit * size of block (implict truncation)
		}
		int sum = codewordLength + blockLength;
		return sum;
	}

	Encoded Simple8b::encode(std::vector<int> &block){
		/* Simple-8b algorithm. Encoded data returned in the form of a vector of codewords (from the prerequisite delta encoding),
		a vector of selectors, and a vector of encoded integers. Bit lengths of these three separate components would then need to be calculated
		in the calcBitLength function. Note each 'block' of data from the simple-8b algorithm contains the selector (4 bits) and the payload (encoded data - 60 bits)*/
		int codeword = block[0];
		// std::cout << codeword << std::endl;
		Encoded encodedBlock;
		std::vector<int> encodedVec;  // Vector which houses result of delta encoding scheme
		//encodedVec.push_back(0); //first value should be 0 as difference from codeword
		for (int i=1; i < block.size(); i++){ // Delta Encoding
			encodedVec.push_back(block[i]-block[i-1]);
		}
		encodedBlock.codewords.push_back(codeword);  // Returning codeword as part of encodedBlock
		int cumBits;
		int ind = 0;  // Index of previously full 64-bit block (initialised at 0)
		std::vector<int> encodedSubBlock;  // Sub-blocks of data - reset every time the payload is filled
		for (int j=0; j < encodedVec.size(); j++){ //for each integer in delta vector

			std::vector<int> tempVec; // Temporary vector - for the purpose of finding the cumulative bit length
			std::vector<int> tempLengthsVec; // Bit lengths of temporary vector - used to find the selector.
			for (int k = ind; k < j; k++){  // From index of previous full payload to current index
				tempVec.push_back(encodedVec[k]);
				tempLengthsVec.push_back(binaryString(encodedVec[k]).length());
			}
			cumBits = calcCumBitLength(tempVec);
			int nextBits;
			if (j != encodedVec.size() - 1){
				nextBits = cumBits + binaryString(encodedVec[j+1]).length(); // Cumulative bits at current index + bit length of next datapoint
			}

			if(nextBits > 60){
				int maxVal = *std::max_element(tempLengthsVec.begin(), tempLengthsVec.end()); //use * as std::max_element returns iterator
				int selector = findSelector(maxVal);
				encodedBlock.codewords.push_back(selector); // Find corresponding selector to max bit length datapoint.
				encodedSubBlock.clear();  // Clears previous entries of sub-block
				for (int l = ind; l < j; l++){
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
		blockLength += maxVal*m_blockSize; //block bit length should be the length of longest bit * size of block (implict truncation)
		return blockLength;
	}

	int Simple8b::calcBitLength(Encoded encBlock){
		/*Overwritten for Simple-8b, as we need to find the bit lengths of the codewords, selectors, and the data in the block */
		int codewordLength = 0;
		codewordLength += binaryString(encBlock.codewords[0]).length(); //get length of binary string of codeword
		for (int i=1; i < encBlock.codewords.size(); i++){ //for each codeword in codewords
			codewordLength += 4;
		}

		int blockLength = 0;
		for (int i=0; i < encBlock.encodedData.size(); i++){ //for each other block in encoded data
			std::vector<int> bitLengths; //maybe optimise later by setting this to size of encodedData.size() and using indexing rather than push_back
			for (int j=0; j < encBlock.encodedData[i].size(); j++){ //for each sub-block in block
				int binLength = binaryString(encBlock.encodedData[i][j]).length();  // For each val in sub-block
				bitLengths.push_back(binLength);
			}
			blockLength += 60;
		}
		int sum = codewordLength + blockLength;
		return sum;
	}