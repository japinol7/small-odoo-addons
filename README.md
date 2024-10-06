## Odoo addons Examples. 

	Small addons examples of Python programming with the Odoo ERP framework.
    You will need to install Odoo 16.0 to use these examples.

	version: 16.0.1.0.0
	author: Joan A. Pinol
	author_nickname: japinol
	author_gitHub: japinol7
	author_twitter: @japinol
	python: 3.12
	PostgreSQL v. tested: 16.4


## Odoo new addon: JAP Sales

### New Features

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for user with group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br /> 
  * One letter A within a solid circle. 

* Create an Invoice from Selected Sale Lines.
  * Only visible for user with group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.


### New icons in order lines

Icon mark to duplicate an order line <br />
<img src="screenshots/icon_1.png" width="60"> <br />

Icon mark to show which lines are duplicated with this feature <br />
<img src="screenshots/icon_2.png" width="60"> <br />


### How it works

Install (Activate) this addon module: JAP Sales. <br />
Note: The following addon modules will be automatically installed:  <br />
JAP Addons Config, JAP Security. <br />  <br />
<img src="screenshots/screenshot1.png" width="980"> <br /> <br />

Activate the 'Role Sales Squad' role for the chosen users <br /> <br />
<img src="screenshots/screenshot2.png" width="980"> <br /> <br />

A Sale or quotation will show a duplicate button for each line <br/>
and an icon mark for a line created by duplication <br /> <br />
<img src="screenshots/screenshot3.png" width="980"> <br /> <br />

Wizard that opens with the button 'Create Invoice from Lines' <br />
You can select which lines to add to the new invoice and add an internal note. <br /> <br />
<img src="screenshots/screenshot4.png" width="980"> <br /> <br />

Invoice created with the Wizard 'Create Invoice from Selected Lines' <br /> <br />
<img src="screenshots/screenshot5.png" width="980"> <br /> <br />
