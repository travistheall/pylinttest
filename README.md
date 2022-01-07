<h1>This is the fake directory I used to check against.</h1>
<h3>DO NOT USE ME</h3>
<h3>Purely to show proof of concept. Ref me to see what is happening</h3>

<p>Feel free to run me to see the test yourself. But, to run in DD proj, clone https://github.com/travistheall/lint_dir.</p>

<h3>proj\lint_dir\Requirements-timestamp.csv</h3>
<table>
    <tr>
        <th>pkg</th>
        <th>used</th>
        <th>what to do</th>
    </tr>
    <tr>
        <td>pandas</td>
        <td>1</td>
        <td>Keep Me</td>
    </tr>
    <tr>
        <td>numpy</td>
        <td>1</td>
        <td>Keep Me</td>
    </tr>
    <tr>
        <td>scipy</td>
        <td>1</td>
        <td>Keep Me</td>
    </tr>
    <tr>
        <td>matplotlib</td>
        <td>0</td>
        <td>Delete Me</td>
    </tr>
    <tr>
        <td>scikitlearn</td>
        <td>0</td>
        <td>Delete Me: <b>Error</b> used as sklearn</td>
    </tr>
    <tr>
        <td>pylint</td>
        <td>0</td>
        <td>Should be used, but lint_dir excluded</td>
    </tr>
</table>

<h3>proj\lint_dir\Not_In_Requirements.csv</h3>
<h6>Still used just not in requirements</h6>
<table>
    <tr>
        <th>pkg</th>
        <th>why</th>
    </tr>
    <tr>
        <td>sklearn</td>
        <td><b>ERROR</b> is in requirements under diff name</td>
    </tr>
    <tr>
        <td>os</td>
        <td>Python Standard Library</td>
    </tr>
    <tr>
        <td>time</td>
        <td>Python Standard Library</td>
    </tr>
    <tr>
        <td>lint_dr</td>
        <td>Project Module</td>
    </tr>
</table>
