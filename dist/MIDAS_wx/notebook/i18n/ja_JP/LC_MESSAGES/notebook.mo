Þ    ]                    ì  [   í  q  I  :   »  "   ö       m   +  g     J   	  ,   L	  I   y	  :   Ã	     þ	     
     9
  3   Q
      
  I   ¦
  X   ð
  ¾   I  3     Y   <  !     i   ¸  v   "  <     1   Ö  ^        g  (   v          ±     Ï     ê  ?     g   D  !   ¬  &   Î  B   õ  %   8  9   ^  ?     *   Ø  5        9  )   L     v      \   /  @     H   Í  P     D   g  &   ¬  2   Ó       &     ,   ¸  =   å  B   #  5   f  @     O   Ý     -  '   M  /   u  +   ¥  W   Ñ  ;   )  -   e           ´      Ô  "   õ  M     3   f  ,     !   Ç    é  Y   ö  $   P     u  ï     6   w     ®  +   M  !   y  ,     6   È     ÿ          (  8   >    w        ¹     T   N"  '   £"     Ë"  r   ä"  R   W#     ª#  L   2$  u   $  s   õ$  -   i%     %     ´%  I   Ñ%  $   &  y   @&  ©   º&    d'  ?   m(  }   ­(  +   +)     W)     ß)  W   f*  V   ¾*     +  	   +  6   ¦+  #   Ý+  L   ,  B   N,  1   ,  {   Ã,     ?-  .   Ô-  4   .  ^   8.  -   .  E   Å.  s   /  F   /  H   Æ/     0  R   .0  <   0    ¾0     Í2  E   P3  y   3  n   4  W   4  3   ×4  @   5  ¡   L5  ;   î5  6   *6  C   a6  L   ¥6  0   ò6  T   #7  b   x7  !   Û7  ;   ý7  ?   98  ,   y8  P   ¦8  D   ÷8  5   <9  '   r9  $   9  '   ¿9  -   ç9  W   :  X   m:  B   Æ:  *   	;  j  4;     <  +   8=     d=  3  =  `   ·>    ?  I   @  -   g@  J   @  5   à@     A  +   )A     UA  W   kA   
        DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib.
         
        Set the tornado compression options for websocket connections.

        This value will be returned from :meth:`WebSocketHandler.get_compression_options`.
        None (default) will disable compression.
        A dict (even an empty one) will enable compression.

        See the tornado docs for WebSocketHandler.get_compression_options for details.
         
    webapp_settings is deprecated, use tornado_settings.
 %d active kernel %d active kernels %s does not exist (bytes/sec)
        Maximum rate at which stream output can be sent on iopub before they are
        limited. (msgs/sec)
        Maximum rate at which messages can be sent on iopub before they are
        limited. (sec) Time window used to 
        check the message and data rate limits. Allow the notebook to be run from root user. Alternatively use `%s` when working on the notebook's Javascript and LESS Cannot bind to localhost, using 127.0.0.1 as default ip
%s Could not set permissions on %s Currently running servers: DEPRECATED use base_url DEPRECATED use the nbserver_extensions dict instead DEPRECATED, use tornado_settings DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib. Deprecated: Use minified JS file or not, mainly use during dev to avoid JS recompilation Dict of Python modules to load as notebook server extensions.Entry values can be used to enable and disable the loading ofthe extensions. The extensions will be loaded in alphabetical order. Don't open the notebook in a browser after startup. ERROR: the notebook server could not be started because no available port could be found. Error loading server extension %s Extra keyword arguments to pass to `set_secure_cookie`. See tornado's set_secure_cookie docs for details. Extra paths to search for serving jinja templates.

        Can be used to override templates from notebook.templates. Extra variables to supply to jinja templates when rendering. Hint: run the following command to set a password If True, each line of output will be a JSON object with the details from the server info file. Interrupted... List currently running notebook servers. No answer for 5s: No such file or directory: %s No such notebook dir: '%r' No web browser found: %s. Notebook servers are configured to only be run with a password. One-time token used for opening a browser.
        Once used, this token cannot be used again.
         Path to search for custom.js, css Permission to listen on port %i denied Please use `%pylab{0}` or `%matplotlib{0}` in the notebook itself. Produce machine-readable JSON output. Reraise exceptions encountered loading server extensions? Running as root is not recommended. Use --allow-root to bypass. Serving notebooks from local directory: %s Set the Access-Control-Allow-Credentials: true header Shutdown confirmed Shutdown this notebook server (%s/[%s])?  Shutting down %d kernels Specify Where to open the notebook on startup. This is the
        `new` argument passed to the standard library method `webbrowser.open`.
        The behaviour is not guaranteed, but depends on browser support. Valid
        values are:
            2 opens a new tab,
            1 opens a new window,
            0 opens in an existing window.
        See the `webbrowser.open` documentation for details.
         Supply SSL options for the tornado HTTPServer.
            See the tornado docs for details. Supply extra arguments that will be passed to Jinja environment. Supply overrides for terminado. Currently only supports "shell_command". Supply overrides for the tornado.web.Application that the Jupyter notebook uses. Support for specifying --pylab on the command line has been removed. Terminals not available (error was %s) The IP address the notebook server will listen on. The Jupyter HTML Notebook.
    
    This launches a Tornado based HTML Notebook Server that serves up an HTML5/Javascript Notebook client. The Jupyter Notebook is running at:
%s The Jupyter Notebook requires tornado >= 4.0 The Jupyter Notebook requires tornado >= 4.0, but you have %s The Jupyter Notebook requires tornado >= 4.0, but you have < 1.1.0 The MathJax.js configuration file that is to be used. The `ignore_minified_js` flag is deprecated and no longer works. The `ignore_minified_js` flag is deprecated and will be removed in Notebook 6.0 The config manager class to use The default URL to redirect to from `/` The directory to use for notebooks and kernels. The file where the cookie secret is stored. The full path to a certificate authority certificate for SSL/TLS client authentication. The full path to a private key file for usage with SSL/TLS. The full path to an SSL/TLS certificate file. The kernel manager class to use. The login handler class to use. The logout handler class to use. The notebook manager class to use. The number of additional ports to try if the specified port is not available. The port %i is already in use, trying another port. The port the notebook server will listen on. The session manager class to use. Token used for authenticating first-time connections to the server.

        When no password is enabled,
        the default is to generate a new, random token.

        Setting to an empty string disables authentication altogether, which is NOT RECOMMENDED.
         Use Control-C to stop this server and shut down all kernels (twice to skip confirmation). Using MathJax configuration file: %s Using MathJax: %s Welcome to Project Jupyter! Explore the various tools available and their corresponding documentation. If you are interested in contributing to the platform, please visit the communityresources section at http://jupyter.org/community.html. Whether to allow the user to run the notebook as root. Whether to trust or not X-Scheme/X-Forwarded-Proto and X-Real-Ip/X-Forwarded-For headerssent by the upstream reverse proxy. Necessary if the proxy handles SSL Writing notebook server cookie secret to %s [all ip addresses on your system] base_project_url is deprecated, use base_url extra paths to look for Javascript notebook extensions interrupted received signal %s, stopping resuming operation... server_extensions is deprecated, use nbserver_extensions Project-Id-Version: Jupyter VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2017-07-08 21:52-0500
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ja_JP
Language-Team: ja_JP <LL@li.org>
Plural-Forms: nplurals=1; plural=0;
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.10.3
 
        éæ¨å¥¨: matplotlib ãæå¹ã«ããã«ã¯ãã¼ãããã¯ã§ %pylab ã¾ãã¯ %matplotlib
        ãå®è¡ãã¦ä¸ããã 
        tornado ã® websocket æ¥ç¶ã®å§ç¸®ãªãã·ã§ã³ãæå®ãã¾ãã

        ãã®å¤ã¯ :meth:`WebSocketHandler.get_compression_options` ããè¿ããã¾ãã
        None (default) ã®å ´åã¯å§ç¸®ã¯ç¡å¹ã«ãªãã¾ãã
        è¾æ¸ (ç©ºã§ãè¯ã) ã®å ´åã¯å§ç¸®ãæå¹ã«ãªãã¾ãã

        è©³ç´°ã¯ tornado ã® WebSocketHandler.get_compression_options ã®ãã­ã¥ã¡ã³ããåç§ã
         
    webapp_settings ã¯éæ¨å¥¨ã§ããtornado_settings ãä½¿ã£ã¦ä¸ããã
 %d åã®ã¢ã¯ãã£ããªã«ã¼ãã« %s ã¯å­å¨ãã¾ãã (bytes/sec)
        ã¹ããªã¼ã åºåãéä¿¡å¶éãããåã« iopub ã§éä¿¡å¯è½ãªæå¤§ã¬ã¼ãã ã¡ãã»ã¼ã¸ãéä¿¡ãããåã« iopub ã§éä¿¡å¯è½ãªæå¤§ã¬ã¼ãã (sec) ãã®ã¦ã£ã³ãã¦ã¯ã¡ãã»ã¼ã¸ã¨ãã¼ã¿ã®å¸¯åãªããã
        ããã§ãã¯ããçºã«ä½¿ç¨ããã¾ãã ãã¼ãããã¯ãrootã¦ã¼ã¶ã¼ããå®è¡ã§ããããã«ããã ãã¼ãããã¯ã® Javascript ã¨ LESS ã§åä½ããå ´åã«ã¯ä»£ããã« `%s` ãä½¿ç¨ãã¦ãã ããã localhost ã§ãã¤ã³ãã§ãã¾ãããããã©ã«ã IP ã¢ãã¬ã¹ã¨ãã¦ 127.0.0.1 ãä½¿ç¨ãã¾ã
%s %s ã®æ¨©éãè¨­å®åºæ¥ã¾ããã§ãã ç¾å¨å®è¡ä¸­ã®ãµã¼ã: éæ¨å¥¨ base_url ã®ä½¿ç¨ éæ¨å¥¨ nbserver_extensions è¾æ¸ãä»£ããã«ä½¿ç¨ãã¦ä¸ãã  éæ¨å¥¨ tornado_settings ã®ä½¿ç¨ ç¡å¹: matplotlib ãæå¹ã«ããã«ã¯ãã¼ãããã¯ã§ %pylab ã¾ãã¯ %matplotlib ãä½¿ç¨ãã¦ä¸ããã éæ¨å¥¨: å§ç¸®ããã JS ãã¡ã¤ã«ãä½¿ç¨ãããã©ãããä¸»ã«éçºä¸­ã« JS ãåã³ã³ãã¤ã«ãããã®ãåé¿ããããã«ä½¿ç¨ãã¾ãã ãã¼ãããã¯ãµã¼ãæ¡å¼µã¨ãã¦ã­ã¼ããã Python ã¢ã¸ã¥ã¼ã«ã®è¾æ¸ãã¨ã³ããªã¼å¤ãä½¿ç¨ãã¦æ¡å¼µã®ã­ã¼ããæå¹ã¾ãã¯ç¡å¹ã«ãããã¨ãã§ãã¾ãã æ¡å¼µå­ã¯ã¢ã«ãã¡ãããé ã«ã­ã¼ãããã¾ãã èµ·åå¾ã«ãã©ã¦ã¶ã§ãã¼ãããã¯ãéããªãã ã¨ã©ã¼: æå¹ãªãã¼ããè¦ä»ãããªãã£ããããã¼ãããã¯ãµã¼ããèµ·åã§ãã¾ããã§ããã ãµã¼ãæ¡å¼µ %s ã®èª­ã¿è¾¼ã¿ã¨ã©ã¼ `set_secure_cookie` ã«æ¸¡ãè¿½å ã®ã­ã¼ã¯ã¼ãå¼æ°ãè©³ç´°ã¯ tornado ã® set_secure_cookie ã®ãã­ã¥ã¡ã³ããåç§ã Jinja ãã³ãã¬ã¼ããæ¢ãçºã®è¿½å ãã¹ã

        notebook.templates ãä¸æ¸ãããçºã«ä½¿ãäºãåºæ¥ã¾ãã jinja ãã³ãã¬ã¼ããã¬ã³ããªã³ã°ããéã«æ¸¡ãããè¿½å ã®å¤æ°ã ãã³ã: ãã¹ã¯ã¼ããè¨­å®ããã«ã¯ä»¥ä¸ã®ã³ãã³ããå®è¡ãã¾ã True ã®å ´åãåºåã®åè¡ã¯ãµã¼ãæå ±ãã¡ã¤ã«ããã®è©³ç´°æå ±ãå«ã JSON ãªãã¸ã§ã¯ãã«ãªãã¾ãã ä¸­æ­... ç¾å¨èµ·åä¸­ã®ãã¼ãããã¯ãµã¼ãã®ä¸è¦§ 5ç§éã«å¿ç­ãããã¾ãã: ãã®æ§ãªãã¡ã¤ã«ã¾ãã¯ãã£ã¬ã¯ããªã¯å­å¨ãã¾ãã: %s ãã¼ãããã¯ãã£ã¬ã¯ããªãè¦ã¤ããã¾ãã: '%r' ã¦ã§ããã©ã¦ã¶ãè¦ã¤ããã¾ãã: %s ãã¼ãããã¯ãµã¼ãã¯ãã¹ã¯ã¼ããè¨­å®ãããå ´åã«ã ãåä½ããããè¨­å®ããã¦ãã¾ãã éãããã©ã¦ã¶ãä»æ§ããã¯ã³ã¿ã¤ã ãã¼ã¯ã³ã
        1åº¦ä½¿ç¨ãããã¨ååº¦ä½¿ç¨ããäºãåºæ¥ã¾ããã
         custom.jsãCSS ãæ¤ç´¢ããããã®ãã¹ ãã¼ã %i ã§å¾æ©ããæ¨©éãããã¾ãã ãã¼ãããã¯ã®ä¸­ã§ `%pylab{0}` ã¾ãã¯ `%matplotlib{0}` ãä½¿ã£ã¦ãã ããã æ©æ¢°ã§èª­ã¿è¾¼ã¿å¯è½ãª JSON åºåã ãµã¼ãæ¡å¼µã®èª­ã¿è¾¼ã¿ä¸­ã«ä¾å¤ãçºçãã¾ãããï¼ root ã¦ã¼ã¶ã§ã®å®è¡ã¯æ¨å¥¨ããã¾ããããã¤ãã¹ããã«ã¯ --allow-root ãä½¿ã£ã¦ä¸ããã ã­ã¼ã«ã«ãã£ã¬ã¯ããªãããã¼ãããã¯ããµã¼ã: %s Access-Control-Allow-Credentials: true ãããã¼ãè¨­å®ãã¾ãã ã·ã£ãããã¦ã³ã®ç¢ºèª ãã®ãã¼ãããã¯ãµã¼ããã·ã£ãããã¦ã³ãã¾ããï¼ (%s/[%s]) %d åã®ã«ã¼ãã«ãã·ã£ãããã¦ã³ãã¦ãã¾ã èµ·åæã«ã©ãã§ãã¼ãããã¯ãéãããæå®ãã¾ããããã¯
        æ¨æºã©ã¤ãã©ãªã®ã¡ã½ãã `webbrowser.open` ã®å¼æ° `new` ã«æ¸¡ããã¾ãã
        åä½ã¯ä¿è¨¼ããã¦ãã¾ããããã©ã¦ã¶ã®ãµãã¼ãã«ãã£ã¦ç°ãªãã¾ãã
        æå¹ãªå¤:
            2 æ°ããã¿ãã§éã
            1 æ°ããã¦ã£ã³ãã¦ã§éã
            0 æ¢ã«ããã¦ã£ã³ãã¦ã§éã
        è©³ç´°ã¯ `webbrowser.open` ã®ãã­ã¥ã¡ã³ããåç§ã
         tornado HTTPServer ã® SSL ãªãã·ã§ã³ãæå®ãã¾ãã
            è©³ããã¯ tornado ã®ãã­ã¥ã¡ã³ããåç§ã Jinja environment ã«æ¸¡ãããè¿½å ã®å¼æ°ãæå®ãã¾ãã terminado ã®ãªã¼ãã¼ã©ã¤ããæå®ãã¾ããç¾æã¯ "shell_command " ã®ã¿ããµãã¼ããã¦ãã¾ãã Jupyterãã¼ãããã¯ãä½¿ç¨ãã tornado.web.Application ã®ãªã¼ãã¼ã©ã¤ããæå®ãã¾ãã ã³ãã³ãã©ã¤ã³ã§ã® --pylab æå®ã¯ãµãã¼ããããªããªãã¾ããã ç«¯æ«ã¯å­å¨ãã¾ãã (%s ã§ã¨ã©ã¼çºç) ãã¼ãããã¯ãµã¼ããå¾ã¡åãã IP ã¢ãã¬ã¹ã The Jupyter HTML Notebook.
    
    HTML5/Javascript Notebook ã¯ã©ã¤ã¢ã³ããæä¾ãã Tornado ãã¼ã¹ã® HTML Notebook ãµã¼ããèµ·åãã¾ãã Jupyter Notebook ã¯ä»¥ä¸ã® URL èµ·åãã¦ãã¾ã:
%s Jupyter Notebook ã¯ tornade 4.0 ä»¥ä¸ãå¿è¦ã§ã Jupyter Notebook ã¯ tornade 4.0 ä»¥ä¸ãå¿è¦ã§ãã %s ã§ã Jupyter Notebook ã¯ tornade 4.0 ä»¥ä¸ãå¿è¦ã§ãã 1.1.0 ä»¥ä¸ã§ã ä½¿ç¨ããã MathJax.js è¨­å®ãã¡ã¤ã«ã `ignore_minified_js` ãã©ã°ã¯éæ¨å¥¨ã§ããæ¢ã«åä½ãã¦ãã¾ããã `ignore_minified_js` ãã©ã°ã¯éæ¨å¥¨ã§ãããã¼ãããã¯ 6.0 ã§ã¯åé¤ããã¾ã è¨­å®ããã¼ã¸ã£ã®ã¯ã©ã¹ `/` ãããªãã¤ã¬ã¯ããããããã©ã«ãã® URL ãã¼ãããã¯ã¨ã«ã¼ãã«ãä½¿ããã£ã¬ã¯ããªã cookie secret ãä¿å­ãããã¡ã¤ã«ã SSL/TLS ã¯ã©ã¤ã¢ã³ãèªè¨¼ç¨ã®èªè¨¼å±è¨¼ææ¸ã¸ã®å®å¨ãªãã¹ã SSL/TLS ã§ä½¿ç¨ããç§å¯éµãã¡ã¤ã«ã¸ã®å®å¨ãªãã¹ã SSL/TLS è¨¼ææ¸ãã¡ã¤ã«ã¸ã®å®å¨ãªãã¹ã ã«ã¼ãã«ããã¼ã¸ã£ã®ã¯ã©ã¹ ã­ã°ã¤ã³ã®ãã³ãã©ã¯ã©ã¹ ã­ã°ã¢ã¦ãã®ãã³ãã©ã¯ã©ã¹ ãã¼ãããã¯ããã¼ã¸ã£ã®ã¯ã©ã¹ æå®ããããã¼ããå©ç¨ã§ããªãå ´åã«è©¦ãè¿½å ã®ãã¼ãã®æ°ã ãã¼ã %i ã¯æ¢ã«ä½¿ç¨ããã¦ãã¾ããä»ã®ãã¼ãã§è©¦ãã¦ä¸ããã ãã¼ãããã¯ãµã¼ããå¾ã¡åããããã¼ãçªå·ã ã»ãã·ã§ã³ããã¼ã¸ã£ã®ã¯ã©ã¹ ãµã¼ãã«æ¥ç¶ããéã«ååã®èªè¨¼ã«ä½¿ããããã¼ã¯ã³ã

        ãã¹ã¯ã¼ãç¡ããæå¹ã«ãªã£ã¦ããå ´å
        ããã©ã«ãå¤ã¯ã©ã³ãã ãªãã¼ã¯ã³ãæ°ããçæããã¾ãã

        ç©ºã®æå­åã«è¨­å®ããã¨èªè¨¼ãå®å¨ã«ç¡å¹ã«ãªãã¾ããããã¯æ¨å¥¨ããã¦ãã¾ããã
         ãµã¼ããåæ­¢ãå¨ã¦ã®ã«ã¼ãã«ãã·ã£ãããã¦ã³ããã«ã¯ Control-C ãä½¿ã£ã¦ä¸ãã(ç¢ºèªãã¹ã­ããããã«ã¯2å)ã ä½¿ç¨ãã MathJax è¨­å®ãã¡ã¤ã«: %s ä½¿ç¨ãã¦ãã MathJax: %s Project Jupyter ã¸ãããã! å©ç¨å¯è½ãªè²ããªãã¼ã«ã¨ããã«å¯¾å¿ãããã­ã¥ã¡ã³ããæ¢ç´¢ãã¦ä¸ããããã©ãããã©ã¼ã ã¸ã®è²¢ç®ã«èå³ãããå ´åã¯ http://jupyter.org/community.html ã® communityresources ã»ã¯ã·ã§ã³ã«ã¢ã¯ã»ã¹ãã¦ãã ããã ã¦ã¼ã¶ã¼ããã¼ãããã¯ã root ã¨ãã¦å®è¡ã§ããããã«ãããã©ããã X-Scheme/X-Forwarded-Proto ããã³ X-Real-Ip/X-Forwarded-For ãããã¼ãã¢ããã¹ããªã¼ã ã®ãªãã¼ã¹ãã­ã­ã·ã«ãã£ã¦éä¿¡ããããã¨ãä¿¡é ¼ãããã©ããããã­ã­ã·ã SSL ãå¦çããå ´åã«å¿è¦ã¨ãªãã¾ãã ãã¼ãããã¯ãµã¼ãã¯ cookie secret ã %s ã«æ¸ãè¾¼ã¿ã¾ã [ã·ã¹ãã ä¸ã®å¨ã¦ã® IP ã¢ãã¬ã¹] base_project_url ã¯éæ¨å¥¨ã§ããbase_url ãä½¿ç¨ãã¦ä¸ããã Javascript ãã¼ãããã¯æ¡å¼µã¸ã®è¿½å ãã¹ ä¸­æ­ãã¾ãã ã·ã°ãã« %s ãåä¿¡ãåæ­¢ãã¾ã æä½ãåéä¸­... server_extensions ãéæ¨å¥¨ã§ãã nbserver_extensions ãä½¿ç¨ãã¦ä¸ããã 