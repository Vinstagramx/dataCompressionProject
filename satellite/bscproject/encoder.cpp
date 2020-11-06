<<<<<<< HEAD
#include <iostream>
#include <bitset>
#include <math.h>
#include <vector>
#include "load.h"
#include <cstdlib>
#include <algorithm>
#include <chrono>
#include <numeric>

struct Encoded
{
/*Enocded is a new data type to store all encoding related stuff into one object - like our [codword, [encoded data]]
on Python but formalised. Codewords is vector to account for multiple codeword schemes, and encoded data is 
multidimensional vector to account for multiple block schemes i.e Golomb/Golomb-based schemes*/
std::vector<int> codewords;
std::vector<std::vector<int>> encodedData;
};

class Encoder
{

private:

	std::string m_fileName;
	int m_sampleNumber;
	std::string m_direction;
	std::vector<int> m_data{};
	std::vector<int> m_sampleIndices{};


public:
	int m_blockSize;
	std::string m_mode;

	Encoder(){ //default constructor
		m_blockSize = 2;
		m_fileName = "test.txt";
		m_sampleNumber = 1000;
		m_direction = "x";
		m_mode = "None";
	}
	explicit Encoder(int bs=2, std::string f="test.txt", int samples=1000, std::string dir="x", std::string mode="None"){
		m_blockSize = bs;
=======
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
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
		m_fileName = f;
		m_sampleNumber = samples;
		m_direction = dir;
		m_mode = mode;
	}
<<<<<<< HEAD
	void setBlockSize(int bs){ //can adjust blocksize inside object so don't need to load data multiple times
		m_blockSize = bs;
	}
	void printParams(){ //debug function to check stuff is working
=======
	void Encoder::setBlockSize(int bs){ //can adjust blocksize inside object so don't need to load data multiple times
		m_blockSize = bs;
	}
	void Encoder::printParams(){ //debug function to check stuff is working
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
		std::cout << "block size: " << m_blockSize << " ";
		std::cout << "file: " << m_fileName << " ";
		std::cout << "sample number: " << m_sampleNumber << " ";
		std::cout << "direction: " << m_direction <<"\n";
	}
<<<<<<< HEAD
	void loadData(){
		csv_load(m_fileName, m_direction, m_data); //return by reference to load data into m_data
		std::cout << "loaded data succesfully \n";
	}
	void printData(){ //debug to check stuff is working
=======
	void Encoder::loadData(){
		csv_load(m_fileName, m_direction, m_data); //return by reference to load data into m_data
		std::cout << "loaded data succesfully \n";
	}
	void Encoder::printData(){ //debug to check stuff is working
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
		for (int i = 0; i < m_data.size(); i++){
			std::cout << m_data[i] << "\n";
		}
	}
<<<<<<< HEAD
	void genSamples(bool random = false){
=======

	float Encoder::getCompressionRatio(){
		return m_compressionRatio;
	}
	void Encoder::genSamples(bool random){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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

<<<<<<< HEAD
	virtual Encoded encode(std::vector<int> &block){ //method to be overwritten by specific encoding schemes later
=======
	Encoded Encoder::encode(std::vector<int> &block){ //method to be overwritten by specific encoding schemes later
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
		Encoded encodedBlock;
		encodedBlock.codewords = std::vector<int>{0}; //initialise this way to avoid seg fault
		encodedBlock.encodedData = std::vector<std::vector<int>>{block}; //ditto
		return encodedBlock;
	}

<<<<<<< HEAD
	std::string binaryString(int n){
=======
	std::string Encoder::binaryString(int n){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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

<<<<<<< HEAD
	virtual int calcBitLength(Encoded encBlock){
=======
	int Encoder::calcBitLength(Encoded encBlock){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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

<<<<<<< HEAD
	int encodeData(){
=======
	int Encoder::encodeData(){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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
<<<<<<< HEAD
		return 0;
	}
};

class Delta : public Encoder
{

public:
	using Encoder::Encoder; //inher
	Encoded encode(std::vector<int> &block){
=======
		m_compressionRatio = compressionRatio;
		return 0;
	}


	Encoded Delta::encode(std::vector<int> &block){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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


<<<<<<< HEAD
};

class Golomb : public Encoder
{
	using Encoder::Encoder;

	std::string unary(int n){
=======


	std::string Golomb::unary(int n){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
		std::string unaryString = "0";
		uint absN = std::abs(n);
		for (int i=0; i < absN; i++){
			unaryString.insert(unaryString.begin(),'1');
		}
<<<<<<< HEAD
		std::cout << "n is: " << n << " and unary is: " << unaryString < "\n";
		return unaryString;
	}

	Encoded encode(std::vector<int> &block){
=======
		//std::cout << "n is: " << n << " and unary is: " << unaryString < "\n";
		return unaryString;
	}

	Encoded Golomb::encode(std::vector<int> &block){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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
<<<<<<< HEAD
			float average = std::accumulate(absBlock.begin(), absBlock.end(), 0.0)/absBlock.size(); //find the average using acucmulate
=======
			float average = std::accumulate(block.begin(), block.end(), 0.0)/block.size(); //find the average using acucmulate
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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

<<<<<<< HEAD
	int calcBitLength(Encoded encBlock){
=======
	int Golomb::calcBitLength(Encoded encBlock){
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
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
<<<<<<< HEAD

};



int main(){
	Golomb d{15, "test.txt", 7000, "x", "min"};
	d.printParams();
	d.loadData();
	auto start = std::chrono::high_resolution_clock::now();
	for (int i=3; i < 100; i++){
		std::cout << "Block Size: " << i << "\n";
		d.setBlockSize(i);
		d.genSamples();
		d.encodeData();
	}
	auto stop = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
	std::cout << "Finished in " << duration.count() << " seconds \n";
}
=======
>>>>>>> a8d2b66f34b91161ded38e26d2f844963d1494b7
