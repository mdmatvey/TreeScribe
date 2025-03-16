class Treescribe < Formula
    desc "A CLI tool to generate directory trees with file contents"
    homepage "https://github.com/mdmatvey/TreeScribe"
    url "https://github.com/mdmatvey/TreeScribe/releases/download/v1.0.0/TreeScribe-v1.0.0.tar.gz"
    sha256 "a8f729f59f3a1b0504fa66bd36acad1f7c61dda01509aac56463482dc185f073"
    license "MIT"
  
    depends_on "python@3.9"
  
    def install
      bin.install "treescribe.py" => "treescribe"
      bin.install ".trscrignore"
      chmod 0755, bin/"treescribe"
    end
  
    test do
      system "#{bin}/treescribe", "--help"
    end
  end