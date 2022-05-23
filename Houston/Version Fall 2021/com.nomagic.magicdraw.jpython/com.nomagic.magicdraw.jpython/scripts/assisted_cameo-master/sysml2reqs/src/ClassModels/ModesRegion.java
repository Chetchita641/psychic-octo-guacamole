package ClassModels;

import java.util.List;

public class ModesRegion {
	
	private List<String> regionState;
	private List<RegionRelation> regionRelation;


	public List<String> getRegionState() {
		return regionState;
	}

	public void setRegionState(List<String> regionState) {
		this.regionState = regionState;
	}

	public List<RegionRelation> getRegionRelation() {
		return regionRelation;
	}

	public void setRegionRelation(List<RegionRelation> regionRelation) {
		this.regionRelation = regionRelation;
	}
}

