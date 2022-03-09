alter table image_contents
	add image_contents_id int not null;

alter table image_contents
	add constraint image_contents_pk
		primary key (image_contents_id);

alter table image_contents modify image_contents_id int auto_increment;


alter table image_usage
	add image_usage_id int not null;

alter table image_usage
	add constraint image_usage_pk
		primary key (image_usage_id);

alter table image_usage modify image_usage_id int auto_increment;

alter table github_packages modify package_id int not null;

alter table github_packages
	add github_package_id int not null;

alter table github_packages drop primary key;

alter table github_packages
	add constraint github_packages_pk
		primary key (github_package_id);

alter table github_packages modify github_package_id int auto_increment;

alter table github_packages
	add constraint github_packages_packages_package_id_fk
		foreign key (package_id) references packages (package_id);

alter table package_dependencies
	add package_dependency_id int auto_increment;

alter table package_dependencies
	add constraint package_dependencies_pk
		primary key (package_dependency_id);

alter table package_dependencies modify package_dependency_id int auto_increment;

