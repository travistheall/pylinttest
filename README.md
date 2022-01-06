<h1>Check files for unused imports and unused packages in requirements.txt</h1>
<h3>Brute force very slow I'm sure</h3>
<div>
    <p>The requirements.txt for this is fake. I used it to check against</p>
    <p>You do need pandas and tqdm though to run this. requirements.txt</p>
</div>
<h3>Known limitation</h3>
<p>If the requirement name is different from the import values then it will be missed. See <b>scikit-learn and sklearn</b>. I don't have an answer to that.</p>
<h3>Steps</h3>
<ol>
    <li>Clone me into the dd repository
        <ul>
            <li>cd /Users/yashbehal/projects/doorstep_django</li>
            <li>git clone https://github.com/travistheall/pylinttest</li>
            <li>mv pylinttest/proj/lint_dir  ../..</li>
            <li>should end up /Users/yashbehal/projects/doorstep_django/lint_dir</li>
            <li>rm -rf pylinttest</li>
            <li>cd /Users/yashbehal/projects/doorstep_django/lint_dir</li>
        </ul>
    </li>
    <li>
        Change pylint_dir variable to this project
        <ul>
            <li>Example:</li>
            <li>pylint_dir = "/Users/yashbehal/projects/doorstep_django/lint_dir"</li>
        </ul>
    </li>
    <li>
        Run
        <ul>
            <li>python main.py</li>
        </ul>
    </li>
    <li>
    Creates 3 files
        <ol>
            <li>out.txt: The output of the pylint command</li>
            <li>not_in_requirements.csv: A csv file with all the packages that are used in the project, but not in requirements.txt</li>
            <ul>
                <li>math, os, project modules, ...</li>
            </ul>
            <li>requirements.csv: A csv file with all the packages from requirements.txt and 1 if used 0 if not</li>
        </ol>
    </li>
</ol>
<h3>Requirements.csv</h3>
<table>
    <tr>
        <th>pkg</th>
        <th>used</th>
        <th>what to do</th>
    </tr>
    <tr>
        <td>pandas</td>
        <td>1</td>
        <td>keep me</td>
    </tr>
    <tr>
        <td>numpy</td>
        <td>0</td>
        <td>delete me</td>
    </tr>
    <tr>
        <td>scipy</td>
        <td>1</td>
        <td>keep me</td>
    </tr>
    <tr>
        <td>matplotlib</td>
        <td>0</td>
        <td>delete me</td>
    </tr>
    <tr>
        <td>scikitlearn</td>
        <td>0</td>
        <td>delete me Error used as sklearn</td>
    </tr>
    <tr>
        <td>pylint</td>
        <td>0</td>
        <td>delete me</td>
    </tr>
</table>

<h3>Not_In_Requirements.csv</h3>
<h6>still used</h6>
<table>
    <tr>
        <th>pkg</th>
        <th>used</th>
        <th>why</th>
    </tr>
    <tr>
        <td>sklearn</td>
        <td>1</td>
        <td>error is in requirements under diff name</td></tr>
    <tr>
        <td>os</td>
        <td>1</td>
        <td>python standard library</td>
    </tr>
    <tr>
        <td>time</td>
        <td>1</td>
        <td>python standard library</td>
    </tr>
    <tr>
        <td>lint_dr</td>
        <td>1</td>
        <td>project module</td>
    </tr>
</table>
