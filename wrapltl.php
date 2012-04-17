<?php
/*
Copyright (c) 2011, Scott C. Livingston
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of Scott C. Livingston nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
?>
<!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
  <title>Wrapper for LTL/automata translators</title>
  <!--<meta name="description" content="hmm...">-->
  <style type="text/css">
pre {
    background-color: #eee;
    font-family: monospace;
}

ul {
    margin-top: -1em;
}

p#footer {
    background-color: #eef;
    font-family: sans-serif;
    font-size: smaller;
}
  </style>
</head>
<body>

<p>
<form action="wrapltl.php" method="POST">
  LTL(<a href="http://www.lsv.ens-cachan.fr/~gastin/ltl2ba/">2BA</a>) formula: <input type="text" name="ltl2ba_formula" size="32" maxlength="255" />
  <input type="submit" name="submit" />
</form>
<hr />
<form action="wrapltl.php" method="POST">
  LTL(<a href="http://www.ltl2dstar.de/">2DSTAR</a>) formula: <input type="text" name="ltl2dstar_formula" size="32" maxlength="255" <? if (isset($_POST["ltl2dstar_formula"])) { echo " value=\"".$_POST["ltl2dstar_formula"]."\" "; } ?> />
  <input type="submit" name="submit" />
  <br />
  <input type="radio" name="automata" value="rabin" checked="" />Rabin<br />
  <input type="radio" name="automata" value="streett" />Streett
  <br />
  <input type="radio" name="output" value="automaton" checked="" />textual representation (cf. <a href="http://www.ltl2dstar.de/docs/ltl2dstar.html#output-format">grammar</a>)<br />
  <input type="radio" name="output" value="dot" />dot description<br />
  <input type="checkbox" name="state_detail" />detailed states<br />
  <input type="checkbox" name="gen_image" />generate graph
</form>
<hr />
</p>

<p>
<pre>
<?php
   if (isset($_POST["ltl2ba_formula"])) {
     $result = system("/home/slivings/opt/bin/ltl2ba -f " . escapeshellarg($_POST["ltl2ba_formula"]));
     $result[strlen($result)-1]="";
     echo $result;
   } elseif (isset($_POST["ltl2dstar_formula"])) {

     // Echo the formula, for completeness...
     echo $_POST["ltl2dstar_formula"];?></pre><hr /><pre><?php
     
     // Manage temporary files.
     $fname = tempnam(".", "wrapltl_tmp_");
     $out_fname = tempnam(".", "wrapltl_tmp_out_");
     file_put_contents($fname, $_POST["ltl2dstar_formula"]);

     // Show detailed states?
     if (isset($_POST["state_detail"])) {
         $state_detail_flag = "yes";
     } else {
         $state_detail_flag = "no";
     }

     // Call ltl2dstar, with appropriate options.
     $sys_result = system("/home/slivings/opt/bin/ltl2dstar --ltl2nba=spin:/home/slivings/opt/bin/ltl2ba --automata=" . $_POST["automata"] . " --detailed-states=" . $state_detail_flag . " --output=" . $_POST["output"] . " " . $fname." ".$out_fname);

     // Output result
     $result = file_get_contents($out_fname);
     echo $result;

     // Generate Graphviz image
     if (isset($_POST["gen_image"])) {
         $tmp_files = glob("tmp/*", GLOB_NOSORT);
         if (count($tmp_files) > 5) {
             $tmp_count = count($tmp_files);
             $num_deleted = 0;
             foreach ($tmp_files as $tmp_img) {
                 unlink($tmp_img);
                 $num_deleted++;
                 if ($tmp_count - $num_deleted < 5)
                     break;
             }
         }
	 $img_fname = "tmp/" . (string)rand() . ".png";
         $sys_result = system("/home/slivings/opt/bin/ltl2dstar --ltl2nba=spin:/home/slivings/opt/bin/ltl2ba --automata=" . $_POST["automata"] . " --detailed-states=" . $state_detail_flag . " --output=dot " . $fname." ".$out_fname);
         $sys_result = system("/home/slivings/opt/bin/dot ".$out_fname." -Tpng -o ".$img_fname);
         ?></pre><img src="<?php echo $img_fname; ?>" /><pre><?php
     }

     // Delete temporary files.
     unlink($fname);
     unlink($out_fname);
   }
?>
</pre>
</p>

<p>
<em>Notes.</em>
<ul>
  <li><a href="http://www.ltl2dstar.de/docs/ltl2dstar.html#ltl-formulas">the input grammar</a> of ltl2dstar;</li>
  <li>graphs are generated using <a href="http://graphviz.org/">Graphviz</a>;</li>
  <li>if execution fails, then output is empty (i.e. no translation!);</li>
</ul>
</p>

<p id="footer">
<a href="http://scottman.net">Scott C. Livingston</a>, 2011.
</p>
</body>
</html>
