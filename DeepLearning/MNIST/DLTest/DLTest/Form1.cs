using OpenCvSharp;
using OpenCvSharp.Dnn;
using OpenCvSharp.Extensions;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DLTest
{
    public partial class Form1 : Form
    {
        VideoCapture capture;
        Net net;

        public Form1()
        {
            InitializeComponent();
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            capture = new VideoCapture();
            capture.Open(0, VideoCaptureAPIs.ANY);
            if (!capture.IsOpened())
            {
                Close();
                return;
            }
            String onnx_model_path = "./model2.onnx";
            net = Net.ReadNetFromONNX(onnx_model_path);
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            timer1.Stop(); // 작업 중간에 다른 이벤트에 간섭받지 않도록 타이머 정지 
            var frameMat = capture.RetrieveMat(); // 캠에서 받아오는 이미지

            // 데이터 전처리
            Cv2.CvtColor(frameMat, frameMat, ColorConversionCodes.BGR2GRAY);
            Cv2.Threshold(frameMat, frameMat, 254, 255, ThresholdTypes.Binary | ThresholdTypes.Otsu);
            Cv2.BitwiseNot(frameMat, frameMat);

            Mat input = CvDnn.BlobFromImage(frameMat, 1 / 255f, new OpenCvSharp.Size(28, 28));
            var outBlobNames = net.GetUnconnectedOutLayersNames();
            var outputBlobs = outBlobNames.Select(tomat => new float[6]).ToArray();
            net.SetInput(input);
            var prob = net.Forward();

            for (int i = 0; i < prob.Rows; i++)
            {
                Cv2.MinMaxLoc(prob.Row(i).ColRange(0, prob.Cols), out _, out OpenCvSharp.Point max);
                Cv2.MinMaxIdx(prob.Row(i).ColRange(0, prob.Cols), out _, out double maxF);
                label1.Text = "결과 : " + max.X.ToString() + " 확률 : " + maxF.ToString("F2");
            }
            var frameBitmap = BitmapConverter.ToBitmap(frameMat);
            pictureBox1.Image?.Dispose();
            pictureBox1.Image = frameBitmap;

            timer1.Start();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            timer1.Start();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            timer1.Stop();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (timer1.Enabled)
            {
                if (textBox1.Text != "")
                {
                    pictureBox1.Image.Save(DateTime.Now.ToString("yyMMddHHmmss-") + textBox1.Text + ".jpg");
                }
            }
        }
    }
}