using System;
using System.IO;
using System.Drawing;
using System.Runtime.InteropServices;
using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.CV.CvEnum;

namespace DetectScaleFaces
{
    class Program
    {

        private const int MAX_SIZE = 400;

        // import needed function from auxiliary dll
        [DllImport(@"pico_fd.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern void DetectFaces(IntPtr frame, float[] rs, float[] cs, float[] ss, float[] qs,
            int minsize, int maxsize, int maxndetections, int detectorID, out int ndetections);

        public static void MakeOutputImages(string imageDir, string outputDir, int faceSize)
        {
            int in_imgs = 0, out_imgs = 0;
            Console.WriteLine("Process started...\n");
            foreach (var imgFile in Directory.GetFiles(imageDir))
            {
                in_imgs++;
                using (var testImg = new Image<Gray, byte>(imgFile)) // enumeration of input images
                {
                    const int maxNDetections = 2048;
                    float[] rs = new float[maxNDetections];
                    float[] cs = new float[maxNDetections];
                    float[] ss = new float[maxNDetections];
                    float[] qs = new float[maxNDetections];
                    float qThreshold = 5f;
                    int nDetections = 0;
                    DetectFaces(testImg, rs, cs, ss, qs, 150, testImg.Height, maxNDetections, 0, out nDetections); // detect face on input image
                    for (int i = 0; i < nDetections; i++)
                    {
                        if (qs[i] < qThreshold) 
                            continue;
                        // extraction of rectangular field with face on input image
                        Rectangle faceRect = new Rectangle((int)(cs[i] - ss[i] / 2), (int)(rs[i] - ss[i] / 2), (int)ss[i], (int)ss[i]);
                        using (var faceImg = testImg.Copy(faceRect).Resize(faceSize, faceSize, INTER.CV_INTER_CUBIC))
                        {
                            faceImg.Save(outputDir + "/" + Path.GetFileNameWithoutExtension(imgFile) + "__.bmp"); // save output image
                            out_imgs++;
                        }
                    }
                }
            }
            Console.WriteLine("Process finished!\n");
            Console.WriteLine("Input images: " + Convert.ToString(in_imgs));
            Console.WriteLine("Output images: " + Convert.ToString(out_imgs));
            Console.WriteLine("Rejected images: " + Convert.ToString(in_imgs - out_imgs) + "\n");
        }

        public static void CleanDirectory(string dirpath)
        {
            System.IO.DirectoryInfo di = new DirectoryInfo(dirpath);
            foreach (FileInfo file in di.GetFiles()) // delete all files
            {
                file.Delete();
            }
            foreach (DirectoryInfo dir in di.GetDirectories()) // delete all subdirectories
            {
                dir.Delete(true);
            }
        }

        public static bool CheckParams(string[] args)
        {
            if (args.Length != 3) // checking the existence of all args
            {
                Console.Title = "Detecting and scaling faces";
                // output error message
                Console.WriteLine("Args should be 3 after calling exe!\n");
                // output info about args
                Console.WriteLine("1st arg - full path to directory with input images");
                Console.WriteLine("2nd arg - full path to directory with output images");
                Console.WriteLine("3rd arg - size of each output image\n");
                return false;
            }
            else
            {
                if (!(Directory.Exists(args[0]))) // checking the existence of folder with input images on path
                {
                    Console.WriteLine("The folder with input images doesn't exist! Please, check full path to this directory!\n");
                    return false;
                }
                int face_size = Convert.ToInt32(args[2], 10); // convert size of each output image
                if ((face_size <= 0) || (face_size > MAX_SIZE)) // validation of value of output image
                {
                    Console.WriteLine("Incorrect value of size for output image! Please, set it right!");
                    Console.WriteLine("This parameter should be more than 0 and less than " + Convert.ToString(MAX_SIZE) + "\n");
                    return false;
                }
                string outdir = args[1];
                // checking for the folder with output images
                if (!(Directory.Exists(outdir))) // create the empty folder for output images, if it doesn't exist
                {
                    Directory.CreateDirectory(outdir);
                }
                // if the folder with output images isn't empty, it is cleaned
                else if ((Directory.GetFiles(outdir).Length != 0) && (Directory.GetDirectories(outdir).Length != 0))
                {
                    CleanDirectory(outdir);
                }
            }
            return true;
        }

        static void Main(string[] args)
        {
            if (CheckParams(args)) {
                int face_size = Convert.ToInt32(args[2], 10);
                MakeOutputImages(args[0], args[1], face_size);
            }
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}