properties_i18n_translator
==========================

This is a simple Python based project to help make i18n and l10n life easier. A UI is provided to translate English .properties files to local .properties file, to extract dictionary file from English .properties file and corresponding local .properties file, or to update (combine) two dictionary file.

.properties files are often used for storing strings for Internationalization and localization in Java related technologies, which are also known as Property Resource Bundles. Contents of .properties file are "key=value" pairs seperated by new line. One can use native2ascii executable provided by Java to convert an local encoded .properties file to unicode encoded .properties file and vice versa. 

The purpose of this project is to deal with three kind of files:

1. English .properties file with 

      "En_key1=En_value1
       En_key2=En_value2
       ...
       En_keyn=En_valuen" 
   as its content.
   
2. Local .properties file with 

      "En_key1=Loc_value1
       En_key2=Loc_value2
       ...
       En_keyn=Loc_valuen" 
   as its content. Loc_value1, Loc_value2, ... Loc_valuen are all unicode(ascii) charactors like "\u5173\u4e8e"(local wors for "关于").
   
3. Dictionary file with 

      "En_value1=Loc_value1
       En_value2=Loc_value2
       ...
       En_valuen=Loc_valuen" 
   as its content.Loc_value1, Loc_value2, ... Loc_valuen are all unicode(ascii) charactors like "\u5173\u4e8e"(local wors for "关于").
   
   
