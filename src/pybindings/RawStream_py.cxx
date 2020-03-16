#include <boost/python.hpp>
#include <sstream>
#include <corsika/RawStream.h>
#include <corsika/RawParticleStream.h>

using namespace boost::python;

struct RawStream
{
    corsika::RawStreamPtr stream;
    RawStream(const std::string& filename)
    {
        stream = corsika::RawStream::Create(filename);
    }
    void close()
    {
        stream.reset();
    }
    bool get_next_block(corsika::Block<corsika::NotThinned>& block)
    {
        return stream->GetNextBlock(block);
    }
    bool get_next_block_th(corsika::Block<corsika::Thinned>& block)
    {
        return stream->GetNextBlock(block);
    }
    void seek_to(size_t to)
    {
        stream->SeekTo(to);
    }
    bool is_open()
    {
        return (bool)stream;
    }
    size_t get_next_position()
    {
        return stream->GetNextPosition();
    }
    corsika::RawParticleStreamPtr particles()
    {
        return corsika::VRawParticleStream::Create(stream);
    }
    corsika::RawParticleStreamPtr particles1(size_t start)
    {
        return corsika::VRawParticleStream::Create(stream, start);
    }
};

void register_RawStream()
{
    docstring_options local_docstring_options(true, true, false);
   
    class_<RawStream,boost::noncopyable>("RawStream", init<std::string>())
    .def("close", &RawStream::close)
    .def("get_next_block", &RawStream::get_next_block)
    .def("get_next_block", &RawStream::get_next_block_th)
    .def("seek_to", &RawStream::seek_to)
    .add_property("is_open", &RawStream::is_open)
    .def("get_next_position", &RawStream::get_next_position)
    .def("particles", &RawStream::particles)
    .def("particles", &RawStream::particles1)
    ;
}
