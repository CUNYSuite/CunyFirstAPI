# Sometimes it's a README fix, or something like that - which isn't relevant for
# including in a project's CHANGELOG for example
declared_trivial = github.pr_title.include? "#trivial"

# Make it more obvious that a PR is a work in progress and shouldn't be merged yet
warn("PR is classed as Work in Progress") if github.pr_title.include? "[WIP]"

# Warn when there is a big PR
warn("Big PR") if git.lines_of_code > 500

# Don't let testing shortcuts get into master by accident
fail("fdescribe left in tests") if `grep -r fdescribe specs/ `.length > 1
fail("fit left in tests") if `grep -r fit specs/ `.length > 1


forgot_tests = !git.modified_files.include?("./cunyfirstapi/tests/tests.py")
if forgot_tests and not declared_trivial
	warn("It appears that you forgot to add a Unit Test to the test file.\n Please add a test and upload the new version.\n The test file can currently be found at: cunyfirstapi/tests/tests.py")
end

## Unit Tests
system("python3 ./cunyfirstapi/tests/tests.py 2> log.txt")
unit_text = File.read("./log.txt")
if not unit_text.include?('OK')
	fail(unit_text)
else
	message("All Unit Test Passed! 🤟")
end
