# Dll

## 一. 综合使用源代码遍历，结合三个工具dumpbin, process explore, depends都有查看可执行程序依赖的dll有什么的功能，对结果进行分析和比较

1. dumpbin

    ~~~shell
    #使用dumpbin查看app.exe的依赖的所有dll
    dumpbin /imports app.exe
    #结果
    Section contains the following imports:
    
        baseLib.dll
                    40D108 Import Address Table
                    412338 Import Name Table
                         0 time date stamp
                         0 Index of first forwarder reference
    
                        0 lib_function
    
        KERNEL32.dll
                    40D000 Import Address Table
                    412230 Import Name Table
                         0 time date stamp
                         0 Index of first forwarder reference
    
                      611 WriteConsoleW
                      44D QueryPerformanceCounter
                      218 GetCurrentProcessId
                      21C GetCurrentThreadId
                      2E9 GetSystemTimeAsFileTime
                      363 InitializeSListHead
                      37F IsDebuggerPresent
                      5AD UnhandledExceptionFilter
                      56D SetUnhandledExceptionFilter
                      2D0 GetStartupInfoW
                      386 IsProcessorFeaturePresent
                      278 GetModuleHandleW
                      217 GetCurrentProcess
                      58C TerminateProcess
                       86 CloseHandle
                      4D3 RtlUnwind
                      261 GetLastError
                      532 SetLastError
                      131 EnterCriticalSection
                      3BD LeaveCriticalSection
                      110 DeleteCriticalSection
                      35F InitializeCriticalSectionAndSpinCount
                      59E TlsAlloc
                      5A0 TlsGetValue
                      5A1 TlsSetValue
                      59F TlsFree
                      1AB FreeLibrary
                      2AE GetProcAddress
                      3C3 LoadLibraryExW
                      462 RaiseException
                      2D2 GetStdHandle
                      612 WriteFile
                      274 GetModuleFileNameW
                      15E ExitProcess
                      277 GetModuleHandleExW
                      1D6 GetCommandLineA
                      1D7 GetCommandLineW
                      109 DecodePointer
                      345 HeapAlloc
                      349 HeapFree
                      175 FindClose
                      17B FindFirstFileExW
                      18C FindNextFileW
                      38B IsValidCodePage
                      1B2 GetACP
                      297 GetOEMCP
                      1C1 GetCPInfo
                      3EF MultiByteToWideChar
                      5FE WideCharToMultiByte
                      237 GetEnvironmentStringsW
                      1AA FreeEnvironmentStringsW
                      514 SetEnvironmentVariableW
                      54A SetStdHandle
                      24E GetFileType
                      2D7 GetStringTypeW
                       9B CompareStringW
                      3B1 LCMapStringW
                      2B4 GetProcessHeap
                      34E HeapSize
                      34C HeapReAlloc
                      19F FlushFileBuffers
                      1EA GetConsoleCP
                      1FC GetConsoleMode
                      523 SetFilePointerEx
                       CB CreateFileW
    
      Summary
    
            2000 .data
            6000 .rdata
            1000 .reloc
            C000 .text
    ~~~

2. process explore(X86)

    用法：点击View，勾选Show Lower Pane，在Lower Pane View中勾选DLL，然后点击需要查看DLL的进程，下面的窗口中就会出现所有与该进程相关的DLL

    查看app.exe的DLL结果

    ![1](img/1.png)

3. depends22(X86)

    用法：File->open，选择app.exe

    结果：

    ![2](img/2.png)

    ![3](img/3.png)

    ![4](img/4.png)

### 比较与分析

使用dumpbin工具查看可执行程序的dll，可以看到app.exe直接依赖的dll及dll对应的函数（应该是被调用的函数）；使用process explore可以看到所有依赖的dll（包括app.exe直接或间接依赖的dll），但是跟depends比起来比较杂乱，层级调用关系不明确；使用depends查看app.exe的依赖dll，不仅可以看到所有的dll，还呈现出了明确的层级调用关系，和dumpbin一样，它也可以呈现出所有dll中被调用的函数于右上方，该dll的所有函数则在右下方显示；通过三种工具的对比，如果要排个使用优先级名次的话：depends>dumpbin>process explore；而dumpbin的优势在于直接在工程的命令行中就可以使用（方便），并且可以显示所有可执行程序直接依赖的dll的被调用函数。

## 二. 三个任务

提示：

link /dll /def:xxx.def

link xxx.lib /out:app.exe

dumpbin /imports xxx.exe

dumpbin /exports xxx.dll

### 1. 会编写dll。把.c文件编译obj文件，把obj文件和lib文件链接为新的dll和lib文件。注意使用def文件定义导出函数。

为什么要写dll？为了方便不开源共享

* 编写dll

创建空工程baseLib，创建源文件base.c，

~~~c
#include<Windows.h>

int internal_function() {
	return 0;
}

int lib_function(char *msg)
{
	// do some works
	MessageBox(0, 
		"msg from base lib",
		msg,
		MB_OK);
	return 0;
}
~~~

头文件baseLib.h

~~~h
#pragma once
int lib_function(char* msg);
~~~

在源文件中新建项，直接把文件名改为exp.def（*.def为模块定义文件），点击确定

~~~def
LIBRARY   baseLib
EXPORTS
    lib_function
;这里只包含了方法lib_function，没有internal_function
~~~

模块定义文件模版

~~~def
LIBRARY   BTREE
EXPORTS
;@表示顺序
   Insert   @1
   Delete   @2
   Member   @3
   Min   @4
~~~

配置：

配置属性->常规->配置类型改为 动态库.dll

链接器->输入->模块定义文件中填写exp.def

重新生成

* 把.c文件编译obj文件，把obj文件和lib文件链接为新的dll和lib文件

打开 工具->VS2017开发人员命令提示符

cd到baseLib目录下，

**注意：可以根据时间来判断是否为新生成文件**

~~~shell
# 将base.c编译为base.obj
cl.exe /c base.c
# 将base.obj和User32.lib（因为lib_function中调用了User32.lib中的MessageBox函数）链接为base.lib和baseLib.dll，base.exp（包含了导出函数和数据项的信息）
link base.obj User32.lib /dll /def:exp.def
~~~

### 2. 编写一个exe,调用第一步生成的dll文件中的导出函数。

方法是

（1）Link是，将第一步生成的lib文件作为输入文件。

（2）保证dll文件和exe文件在同一目录，或者dll 文件在系统目录

新建项目app

编写源文件app.c

~~~c
int main() {
	lib_function("call a dll");
	return 0;
}
~~~

打开 工具->VS2017开发人员命令提示符

cd到app目录下

~~~shell
#编译app.c为app.obj
cl.exe /c app.c
#将base.lib复制到app项目目录下
copy ..\baseLib\base.lib
#链接app.obj和base.lib为app.exe
link app.obj base.lib /out:app.exe
#将dll复制到app项目目录下
copy ..\baseLib\baseLib.dll
#运行
app.exe
~~~

项目中运行的办法：

右键项目打开属性->在VC++包含目录中点编辑->新行->选择baseLib文件夹（它是包含baseLib.h的文件夹，这么做是为了在app.c中可以用尖括号include baseLib.h）

在链接器->输入->附加依赖项中点编辑->写入目录..\baseLib\base.lib

然后在app.c中写入（其实不写也可以运行，根据上述命令行操作可知，链接时需要base.lib，所以只配置base.lib完全是可以正常运行的）

~~~c
#include <baseLib.h>
~~~

### 3. 第二步调用方式称为load time 特点是exe文件导入表中会出先需要调用的dll文件及函数名，并且link生成exe时，需明确输入lib文件。还有一种调用方式称为run time，参考链接，使用run time的方式，调用dll的导出函数。包括系统API和第一步自行生成的dll，都要能成功调用。

[参考链接](https://docs.microsoft.com/zh-cn/windows/win32/dlls/using-run-time-dynamic-linking)

新建工程RunTimeApp，创建rapp.c

~~~c
#include <windows.h> 
#include <stdio.h> 

typedef int(__cdecl *MYPROC)(LPWSTR);

int main() {
	HINSTANCE hinstLib;
	MYPROC ProcAdd;
	BOOL fFreeResult, fRunTimeLinkSuccess = FALSE;

	// Get a handle to the DLL module.

	hinstLib = LoadLibrary(TEXT("baseLib.dll"));

	// If the handle is valid, try to get the function address.

	if (hinstLib != NULL)
	{
		ProcAdd = (MYPROC)GetProcAddress(hinstLib, "lib_function");

		// If the function address is valid, call the function.

		if (NULL != ProcAdd)
		{
			fRunTimeLinkSuccess = TRUE;
			(ProcAdd)("call a dll");//这里传入函数lib_function的参数
		}
		// Free the DLL module.

		fFreeResult = FreeLibrary(hinstLib);
	}

	// If unable to call the DLL function, use an alternative.
	if (!fRunTimeLinkSuccess)
		printf("Message printed from executable\n");
	return 0;
}
~~~

![5](img/5.png)