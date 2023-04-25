function [dmrsSymbols, dmrsIndices, ptrsSymbols, ptrsIndices] = gen_pdschdmrs(cfg)
    carrier = nrCarrierConfig;
    carrier.SubcarrierSpacing = 120;
    carrier.CyclicPrefix = 'normal';
    carrier.NSizeGrid = 132;
    carrier.NStartGrid = 0;

    % Configure the physical downlink shared channel parameters
    pdsch = nrPDSCHConfig;
    pdsch.NSizeBWP = [];   % Empty implies that the value is equal to NSizeGrid
    pdsch.NStartBWP = [];  % Empty implies that the value is equal to NStartGrid
    pdsch.MappingType = cfg.MappingType; % PDSCH mapping type ('A' or 'B')
    pdsch.DMRS.DMRSTypeAPosition = cfg.DMRSTypeAPosition;      % 2 or 3
    pdsch.DMRS.DMRSLength = cfg.DMRSLength;             % 1 or 2
    pdsch.DMRS.DMRSAdditionalPosition = cfg.DMRSAdditionalPosition; % 0...3
    pdsch.PRBSet = vertcat(cfg.PRBSet{:});   % Allocate the complete carrier
    pdsch.SymbolAllocation = [cfg.SymbolAllocation{1} cfg.SymbolAllocation{2}]; % Symbol allocation [S L]
    pdsch.DMRS.DMRSConfigurationType = cfg.DMRSConfigurationType; % 1 or 2
    pdsch.DMRS.DMRSPortSet = 0;
    pdsch.DMRS.NumCDMGroupsWithoutData = 1; % 1 corresponds to CDM group number 0
    pdsch.DMRS.NIDNSCID = cfg.NIDNSCID; % Use empty to set it to NCellID of the carrier
    pdsch.DMRS.NSCID = cfg.NSCID;    % 0 or 1
    pdsch.NumLayers = numel(pdsch.DMRS.DMRSPortSet);

    pdsch.EnablePTRS = cfg.EnablePTRS;
    pdsch.RNTI = 1;
    pdsch.PTRS.TimeDensity = cfg.PTRSTimeDensity;
    pdsch.PTRS.FrequencyDensity = cfg.PTRSFrequencyDensity; % 2 or 4
    pdsch.PTRS.REOffset = cfg.PTRSREOffset;      % '00', '01', '10', '11'
    pdsch.PTRS.PTRSPortSet = min(pdsch.DMRS.DMRSPortSet);

    % Generate DM-RS indices
    dmrsSymbols = nrPDSCHDMRS(carrier, pdsch);
    dmrsIndices = nrPDSCHDMRSIndices(carrier, pdsch);

    ptrsSymbols = nrPDSCHPTRS(carrier, pdsch);
    ptrsIndices = nrPDSCHPTRSIndices(carrier, pdsch);
end

