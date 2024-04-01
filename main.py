from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
from resources.functions.functions import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Dialog(ctk.CTkToplevel):
    def __init__(self, title, mainlabel, textlabels, fgcolor):
        super().__init__()

        self.title(title)
        self.attributes("-topmost", True)
        self.textEntry = []
        self.grab_set()

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        positionRight = int(self.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 2 - windowHeight / 2)

        self.geometry("+{}+{}".format(positionRight, positionDown))

        mainLabel = ctk.CTkLabel(self, text=mainlabel, font=("Trebuchet MS Bold", 16))
        mainLabel.pack()
        mainFrame = ctk.CTkFrame(self, fg_color=fgcolor)
        mainFrame.pack(padx=5, pady=5)

        for i in range(len(textlabels)):
            tmpFrame = ctk.CTkFrame(mainFrame, fg_color=fgcolor)
            tmpFrame.pack()
            textLabel = ctk.CTkLabel(
                tmpFrame, text=textlabels[i], font=("Trebuchet MS Bold", 16)
            )
            textLabel.grid(row=0, column=0, padx=5, pady=5)
            self.textEntry.append(ctk.CTkEntry(tmpFrame, font=("Trebuchet MS", 16)))
            self.textEntry[i].grid(row=0, column=1, padx=5, pady=5)

        buttonFrame = ctk.CTkFrame(self, fg_color=fgcolor)
        buttonFrame.pack()
        SubmitButton = ctk.CTkButton(
            buttonFrame,
            text="OK",
            command=lambda: self.apply(len(textlabels)),
            width=50,
            font=("Trebuchet MS Bold", 16),
        )
        SubmitButton.grid(row=0, column=0, padx=5, pady=5)
        self.bind("<Return>", lambda event: SubmitButton.invoke())
        CancelButton = ctk.CTkButton(
            buttonFrame,
            text="Cancel",
            command=lambda: self.destroy(),
            width=50,
            font=("Trebuchet MS Bold", 16),
        )
        CancelButton.grid(row=0, column=1, padx=5, pady=5)

        self._user_input = []

    def apply(self, n):
        for i in range(n):
            self._user_input.append(self.textEntry[i].get())
        self.destroy()

    def get_input(self):
        self.wait_window()
        return self._user_input


class App(ctk.CTk):
    def __init__(self):
        self.inputimage = None
        self.ced = None

        super().__init__()
        self.home_text_var = ctk.StringVar()

        # Configuration
        self.title("Canny Edge Detection Application")

        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 1000
        window_height = 755

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(side="top", anchor="n", fill="x")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.header_sub_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.header_sub_frame.pack(side="right", anchor="ne")

        self.home_button = ctk.CTkButton(
            self.header_sub_frame,
            width=40,
            height=40,
            corner_radius=8,
            text="",
            hover_color="red",
            command=lambda title="home": self.display_page(title),
            image=ctk.CTkImage(
                light_image=Image.open("./resources/images/home.png"), size=(40, 40)
            ),
        )
        self.home_button.pack(side="right", anchor="ne", padx=5, pady=13)

        button_exit = ctk.CTkButton(
            self.header_sub_frame,
            width=40,
            height=40,
            corner_radius=8,
            text="",
            fg_color="red",
            hover_color="#FF0",
            command=self.quit,
            image=ctk.CTkImage(
                light_image=Image.open("./resources/images/exit.png"), size=(40, 40)
            ),
        )
        button_exit.pack(side="right", anchor="ne", pady=13)

        self.home_text_var.set(value="Image Processing\nCanny Edge Detection")

        main_label = ctk.CTkLabel(
            self.header_frame,
            textvariable=self.home_text_var,
            font=("Trebuchet MS Bold", 30),
            text_color="red",
        )
        main_label.place(relx=0.5, rely=0.5, anchor="center")

        button_images = [
            "./resources/images/inputimage.png",
            "./resources/images/grayscale.png",
            "./resources/images/smoothing.png",
            "./resources/images/nabla.png",
            "./resources/images/nonmaxsupp.png",
            "./resources/images/doubletreshold.png",
            "./resources/images/hysteresis.png",
        ]
        button_titles = [
            "Input an image",
            "Gray Scalling",
            "Gaussian Filter",
            "Intensity\nGradient",
            "Non Maximum\nSuppression",
            "Double\nThreshold",
            "Hysteresis",
        ]

        for i in range(len(button_images)):
            button = ctk.CTkButton(
                self.left_frame,
                command=lambda title=button_titles[i]: self.display_page(title),
                corner_radius=6,
                text=button_titles[i],
                compound="top",
                font=("Trebuchet MS Bold", 16),
                hover_color="red",
                image=ctk.CTkImage(
                    light_image=Image.open(button_images[i]), size=(80, 50)
                ),
            )
            button.pack(padx=1, pady=2)

        self.display_page("home")

    def display_page(self, button_title):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if button_title == "home":
            self.home_text_var.set(value="Image Processing\nCanny Edge Detection")
            self.inputimage = None

            dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

            dataFrame.rowconfigure(0, weight=1)
            dataFrame.rowconfigure(1, weight=2)
            dataFrame.rowconfigure(3, weight=2)
            dataFrame.rowconfigure(4, weight=1)
            dataFrame.rowconfigure(5, weight=1)
            dataFrame.rowconfigure(6, weight=1)

            subdataFrame = []

            for i in range(6):
                subdataFrame.append(ctk.CTkFrame(dataFrame, fg_color="transparent"))

            tempLab = ctk.CTkLabel(
                subdataFrame[0],
                text="Parameters :",
                font=("Trebuchet MS Bold", 34),
                text_color="red",
            )
            tempLab.pack(pady=40)

            paramLab1 = ctk.CTkLabel(
                subdataFrame[1],
                text="Gaussian Kernel Size : ",
                font=("Trebuchet MS Bold", 24),
            )
            paramLab1.pack()

            kernelSizeLabel = ctk.CTkLabel(
                subdataFrame[1],
                text=f"{CannyEdgeDetector.KERNEL_SIZE}",
                font=("Trebuchet MS Bold", 24),
                text_color="red",
            )
            kernelSizeLabel.pack()

            def changeKernelSize(x):
                CannyEdgeDetector.KERNEL_SIZE = round(x)
                kernelSizeLabel.configure(text=str(CannyEdgeDetector.KERNEL_SIZE))

            GKSize = ctk.CTkSlider(
                subdataFrame[1],
                from_=5,
                to=10,
                number_of_steps=5,
                command=lambda x: changeKernelSize(GKSize.get()),
                progress_color="red",
                button_color="black",
                button_hover_color="grey",
            )
            GKSize.set(CannyEdgeDetector.KERNEL_SIZE)
            GKSize.pack()

            paramLab2 = ctk.CTkLabel(
                subdataFrame[2],
                text="Kernel Standard Deviation : ",
                font=("Trebuchet MS Bold", 24),
            )
            paramLab2.pack()

            kernelSDLabel = ctk.CTkLabel(
                subdataFrame[2],
                text=f"{CannyEdgeDetector.KERNEL_SD}",
                font=("Trebuchet MS Bold", 24),
                text_color="red",
            )
            kernelSDLabel.pack()

            def changeKernelSD(x):
                CannyEdgeDetector.KERNEL_SD = round(x, 2)
                kernelSDLabel.configure(text=str(CannyEdgeDetector.KERNEL_SD))

            GKsd = ctk.CTkSlider(
                subdataFrame[2],
                from_=0.5,
                to=5,
                command=lambda x: changeKernelSD(GKsd.get()),
                progress_color="red",
                button_color="black",
                button_hover_color="grey",
            )
            GKsd.set(CannyEdgeDetector.KERNEL_SD)
            GKsd.pack()

            paramLab3 = ctk.CTkLabel(
                subdataFrame[3],
                text="High Treshold Ratio :",
                font=("Trebuchet MS Bold", 24),
            )
            paramLab3.pack()

            HighTRatioLabel = ctk.CTkLabel(
                subdataFrame[3],
                text=f"{CannyEdgeDetector.HIGH_THRESHOLD_RATIO}",
                font=("Trebuchet MS Bold", 24),
                text_color="red",
            )
            HighTRatioLabel.pack()

            def changeHighTRation(x):
                CannyEdgeDetector.HIGH_THRESHOLD_RATIO = round(x, 2)
                HighTRatioLabel.configure(
                    text=str(CannyEdgeDetector.HIGH_THRESHOLD_RATIO)
                )

            HighTRatio = ctk.CTkSlider(
                subdataFrame[3],
                from_=0.0,
                to=0.9,
                command=lambda x: changeHighTRation(HighTRatio.get()),
                progress_color="red",
                button_color="black",
                button_hover_color="grey",
            )
            HighTRatio.set(CannyEdgeDetector.HIGH_THRESHOLD_RATIO)
            HighTRatio.pack()

            paramLab4 = ctk.CTkLabel(
                subdataFrame[4],
                text="Low Treshold Ratio :",
                font=("Trebuchet MS Bold", 24),
            )
            paramLab4.pack()

            LowTRatioLabel = ctk.CTkLabel(
                subdataFrame[4],
                text=f"{CannyEdgeDetector.LOW_THRESHOLD_RATIO}",
                font=("Trebuchet MS Bold", 24),
                text_color="red",
            )
            LowTRatioLabel.pack()

            def changeLowTRation(x):
                CannyEdgeDetector.LOW_THRESHOLD_RATIO = round(x, 2)
                LowTRatioLabel.configure(
                    text=str(CannyEdgeDetector.LOW_THRESHOLD_RATIO)
                )

            LowTRatio = ctk.CTkSlider(
                subdataFrame[4],
                from_=0.05,
                to=0.6,
                command=lambda x: changeLowTRation(LowTRatio.get()),
                progress_color="red",
                button_color="black",
                button_hover_color="grey",
            )
            LowTRatio.set(CannyEdgeDetector.LOW_THRESHOLD_RATIO)
            LowTRatio.pack()

            paramLab5 = ctk.CTkLabel(
                subdataFrame[5], text="Weak Pixek : ", font=("Trebuchet MS Bold", 24)
            )
            paramLab5.pack()

            WeakPixelLabel = ctk.CTkLabel(
                subdataFrame[5],
                text=f"{CannyEdgeDetector.WEAK_PIXEL}",
                font=("Trebuchet MS Bold", 24),
                text_color="red",
            )
            WeakPixelLabel.pack()

            def changeWeakPixel(x):
                CannyEdgeDetector.WEAK_PIXEL = round(x)
                WeakPixelLabel.configure(text=str(CannyEdgeDetector.WEAK_PIXEL))

            WeakPixel = ctk.CTkSlider(
                subdataFrame[5],
                from_=0,
                to=255,
                command=lambda x: changeWeakPixel(WeakPixel.get()),
                progress_color="red",
                button_color="black",
                button_hover_color="grey",
            )
            WeakPixel.set(CannyEdgeDetector.WEAK_PIXEL)
            WeakPixel.pack()

            for frame in subdataFrame:
                frame.pack(fill="x", padx=10, pady=5)

            dataFrame.pack(fill="x", padx=5, pady=15)

        elif button_title == "Input an image":
            self.home_text_var.set(value="Input Image : ")

            # Open the file dialog
            file_path = ctk.filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.png")]
            )

            if file_path:
                self.inputimage = image(file_path)
                self.ced = CannyEdgeDetector(image(file_path))

                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(self.ced.img.originaldata)

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Gray Scalling": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)
            else:
                self.display_page("home")

        elif button_title == "Gray Scalling":
            self.home_text_var.set(value="Gray Scalled Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(self.ced.img.data, cmap="gray", vmin=0, vmax=255)

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Gaussian Filter": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)

        elif button_title == "Gaussian Filter":
            self.home_text_var.set(value="Gaussian Filtered Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(self.ced.gaussianFilter().data, cmap="gray", vmin=0, vmax=255)

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Intensity\nGradient": self.display_page(
                        title
                    ),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)

        elif button_title == "Intensity\nGradient":
            self.home_text_var.set(value="Intensity Gradient Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(self.ced.intensityGradient()[0], cmap="gray", vmin=0, vmax=255)

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Non Maximum\nSuppression": self.display_page(
                        title
                    ),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)

        elif button_title == "Non Maximum\nSuppression":
            self.home_text_var.set(value="Non Maximum Suppressed Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(
                    self.ced.nonMaximumSuppression().data, cmap="gray", vmin=0, vmax=255
                )

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Double\nThreshold": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)

        elif button_title == "Double\nThreshold":
            self.home_text_var.set(value="Double Threshold Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(self.ced.doubleThreshold().data, cmap="gray", vmin=0, vmax=255)

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="Hysteresis": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)

        elif button_title == "Hysteresis":
            self.home_text_var.set(value="Hysteresis Image : ")
            if self.inputimage:
                dataFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")

                plotFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")

                frame_width = plotFrame.winfo_width()
                frame_height = plotFrame.winfo_height()

                fig = Figure(figsize=(frame_width * 7, frame_height * 7))
                a = fig.add_subplot(111)

                fig.subplots_adjust(
                    left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0
                )

                a.imshow(
                    self.ced.hystheresisTracking().data, cmap="gray", vmin=0, vmax=255
                )

                canvas = FigureCanvasTkAgg(fig, master=plotFrame)
                canvas.draw()
                canvas.get_tk_widget().pack()

                plotFrame.pack(fill="both", padx=5, pady=5, expand=True)

                buttonsFrame = ctk.CTkFrame(dataFrame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=10)

                next_step_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="#FF0",
                    command=lambda title="home": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/next.png"),
                        size=(70, 70),
                    ),
                )
                next_step_button.pack(side="right", anchor="ne", padx=20, pady=10)

                buttonsFrame.pack(side="bottom", padx=5, pady=5)

                dataFrame.pack(fill="both", padx=5, pady=5, expand=True)

            else:
                Warning_Label = ctk.CTkLabel(
                    self.main_frame,
                    text="ACHTUNG !\nEingabebild nicht gefunden !\n-------\nWarning !\nInput image not found !\n-------\nAttention !\nImage d'entrée introuvable !",
                    font=("Trebuchet MS Bold", 26),
                    text_color="red",
                    corner_radius=10,
                )
                Warning_Label.pack(side="top", pady=60)
                self.home_text_var.set(value="You need to re/input an image because : ")
                buttonsFrame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                change_button = ctk.CTkButton(
                    buttonsFrame,
                    width=70,
                    height=70,
                    corner_radius=8,
                    text="",
                    fg_color="lightblue",
                    hover_color="green",
                    command=lambda title="Input an image": self.display_page(title),
                    image=ctk.CTkImage(
                        light_image=Image.open("./resources/images/changeimage.png"),
                        size=(70, 70),
                    ),
                )
                change_button.pack(side="left", anchor="ne", padx=20, pady=20)
                buttonsFrame.pack(side="bottom", padx=5, pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
