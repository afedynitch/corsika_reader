/**
 \file
 Implement raw CORSIKA file
 
 \author Lukas Nellen
 \version $Id$
 \date 08 Dec 2003
 */
#include <string>
#include <sstream>
#include <corsika/RawStream.h>
#include <corsika/FileStream.h>

#ifdef __GNUC__
#define PACK( __Declaration__ ) __Declaration__ __attribute__((__packed__))
#endif

#ifdef _MSC_VER
#define PACK( __Declaration__ ) __pragma( pack(push, 1) ) __Declaration__ __pragma( pack(pop))
#endif


namespace corsika
{
    template <typename Thinning, typename Padding> struct RawStreamT: RawStream
    {
        PACK(struct DiskBlock
        {
            Padding padding_start;
            Block<Thinning>  fBlock[kSubBlocksPerBlock];
            Padding padding_end;
        });
        
        boost::shared_ptr<FileStream> file;
        std::string filename;
        size_t current_block;
        size_t current_disk_block;
        bool buffer_valid;
        DiskBlock buffer;
        
        RawStreamT(boost::shared_ptr<FileStream> file, std::string filename, int64_t len64): file(file), filename(filename), current_block(0), current_disk_block(0)
        {
            *reinterpret_cast<int64_t*>(&buffer) = len64; // Copy value over
            buffer_valid = file->read(sizeof(DiskBlock) - 8, (char*)&buffer + 8) > 0;
        }
        bool valid()
        {
            return buffer_valid && buffer.fBlock[0].IsRunHeader() && (buffer.padding_start == buffer.padding_end);
        }
        
        template<typename T> bool read_block(T& block)
        {
            return false;
        }
        bool read_block(Block<Thinning>& block)
        {
            if (!buffer_valid)
            {
                if (!ReadDiskBlock())
                    return false;
            }
            
            block = buffer.fBlock[current_disk_block];
            if (++current_disk_block >= kSubBlocksPerBlock)
            {
                current_block++;
                current_disk_block = 0;
                buffer_valid = false;
            }
            return true;
        }
        bool GetNextBlock(Block<Thinned>& theBlock)
        {
            return read_block(theBlock);
        }
        bool GetNextBlock(Block<NotThinned>& theBlock)
        {
            return read_block(theBlock);
        }
        
        /// Number of the block read by the next call to GetNextBlock
        size_t GetNextPosition() const
        {
            return current_disk_block + kSubBlocksPerBlock * current_block;
        }
        
        bool IsSeekable() const { return true; }
        
        /// Seek to a given block, the next block will be \a thePosition
        void SeekTo(size_t thePosition)
        {
            size_t newBlockNumber = thePosition / kSubBlocksPerBlock;
            size_t newIndexInBlock = thePosition % kSubBlocksPerBlock;
            //if (newBlockNumber == fCurrentBlockNumber && newIndexInBlock == fIndexInDiskBlock) return
            if (file->seekable)
            {
                current_block = newBlockNumber;
                buffer_valid   = false;
                current_disk_block   = newIndexInBlock;
                file->seek(current_block * sizeof(DiskBlock));
            }
            else
            {
                if (GetNextPosition() > thePosition)
                {
                    file.reset(FileStream::open(filename.c_str()));
                    if (!file) throw IOException("Failed in dumb seek");
                    current_block = 0;
                    current_disk_block = 0;
                    buffer_valid = false;
                }
                Block<Thinning> block;
                while (thePosition > 0 && thePosition > GetNextPosition())
                    GetNextBlock(block);
            }
        }
        bool IsThinned() const
        {
            return Thinning::kWordsPerSubBlock == Thinned::kWordsPerSubBlock;
        }
        bool ReadDiskBlock()
        {
            if (file->read(sizeof(DiskBlock), &buffer) <= 0) return false;
            if (buffer.padding_start != buffer.padding_end) throw IOException("Padding mismatch\n");
            buffer_valid = true;
            return true;
        }
    };
    template <typename Thinning, typename Padding>
    RawStreamPtr create_stream(boost::shared_ptr<FileStream> file, std::string filename, int64_t len64)
    {
        auto ptr = new RawStreamT<Thinning, Padding>(file, filename, len64);
        if (ptr->valid()) return RawStreamPtr(ptr);
        delete ptr;
        throw IOException("Not a valid corsika file\n");
    }
    
    RawStreamPtr RawStream::Create(const std::string& filename)
    {
        boost::shared_ptr<FileStream> file(FileStream::open(filename.c_str()));
        if (!file) throw IOException("Error opening Corsika file '" + filename + "'.\n");
        
        int64_t len64;
        file->read(8, &len64);
        int32_t len32 = *reinterpret_cast<int32_t*>(&len64);
        
        const int thinned_size = sizeof(GenericBlock<Thinned>) * kSubBlocksPerBlock;
        const int not_thinned_size = sizeof(GenericBlock<NotThinned>) * kSubBlocksPerBlock;

        if (len64 == thinned_size)
            return create_stream<Thinned, int64_t>(file, filename, len64); // 64bit thinned
        else if (len64 == not_thinned_size)
            return create_stream<NotThinned, int64_t>(file, filename, len64); // 64bit not-thinned
        else if (len32 == thinned_size)
            return create_stream<Thinned, int32_t>(file, filename, len64); // 32bit thinned
        else if (len32 == not_thinned_size)
            return create_stream<NotThinned, int32_t>(file, filename, len64); // 32bit not-thinned
        
        throw IOException("Can't determine type of corsika file\n");
    }
}
